from ctypes import *
from my_debugger_defines import *

import sys
import time
kernel32 = windll.kernel32


class debugger():

    def __init__(self):
        self.h_process = None
        self.pid = None
        self.debugger_active = False
        self.h_thread = None
        self.context = None
        self.breakpoints = {}
        self.first_breakpoint = True
        self.hardware_breakpoints = {}

        print('start with lasterror', GetLastError())
        kernel32.SetLastError(0)

        # Here let's determine and store
        # the default page size for the system
        # determine the system page size.
        system_info = SYSTEM_INFO()
        kernel32.GetSystemInfo(byref(system_info))
        self.page_size = system_info.dwPageSize

        # TODO: test
        self.guarded_pages = []
        self.memory_breakpoints = {}

    def load(self, path_to_exe):

        # dwCreation flag determines how to create the process
        # set creation_flags = CREATE_NEW_CONSOLE if you want
        # to see the calculator GUI
        creation_flags = DEBUG_PROCESS

        # instantiate the structs
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        # The following two options allow the started process
        # to be shown as a separate window. This also illustrates
        # how different settings in the STARTUPINFO struct can affect
        # the debuggee.
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0

        # We then initialize the cb variable in the STARTUPINFO struct
        # which is just the size of the struct itself
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):

            print("[*] We have successfully launched the process!")
            print("[*] The Process ID I have is: %d" %
                  process_information.dwProcessId)
            self.pid = process_information.dwProcessId
            self.h_process = self.open_process(process_information.dwProcessId)
            self.debugger_active = True
        else:
            print("[*] Error with error code %d." % kernel32.GetLastError())

    def open_process(self, pid):

        # PROCESS_ALL_ACCESS = 0x0x001F0FFF
        # h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS,False,pid)
        # print(f"h_process {h_process}")
        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

        return h_process

    def attach(self, pid):
        self.h_process = self.open_process(pid)

        Wow64Process = c_ushort(0xffff)
        kernel32.IsWow64Process(self.h_process, byref(Wow64Process))

        # We attempt to attach to the process
        # if this fails we exit the call
        if kernel32.DebugActiveProcess(pid):
            print(
                f'====   attached succeed !! [ Wow64Process = {Wow64Process.value} ]   ====')
            self.debugger_active = True
            self.pid = int(pid)
            # self.run()
        else:
            print(
                f"Unable to attach to the process. lasterror = {GetLastError()}")

    def run(self, debug_action):

        # Now we have to poll the debuggee for
        # debugging events
        while self.debugger_active == True:
            self.get_debug_event(debug_action)

    def get_debug_event(self, debug_action):

        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        Milliseconds = INFINITE
        Milliseconds = 100
        if kernel32.WaitForDebugEvent(byref(debug_event), Milliseconds):

            # grab various information with regards to the current exception.
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(h_thread=self.h_thread)
            self.debug_event = debug_event

            print("DebugEvent Code: %d TID: %d" %
                  (debug_event.dwDebugEventCode, debug_event.dwThreadId))

            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:

                self.exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = debug_event.u.Exception.ExceptionRecord.ExceptionAddress
                print(
                    f'  > EXCEPTION_DEBUG_EVENT [ exception=0x{self.exception:x} ]')
                print(
                    f"  > Exception address: 0x{self.exception_address:016x}")

                # call the internal handler for the exception event that just occured.
                if self.exception == EXCEPTION_ACCESS_VIOLATION:
                    print("    > # Access Violation Detected.")
                elif self.exception == EXCEPTION_BREAKPOINT:
                    print("    > # Breakpoint Detected.")
                    print(
                        f'    > Rip = 0x{self.context.Rip:016x} Rax = 0x{self.context.Rax:016x}')
                    continue_status = self.exception_handler_breakpoint()
                elif self.exception == EXCEPTION_GUARD_PAGE:
                    print("    > # Guard Page Access Detected.")
                    print(
                        f'    > Rip = 0x{self.context.Rip:016x} Rax = 0x{self.context.Rax:016x}')
                elif self.exception == EXCEPTION_SINGLE_STEP:
                    self.exception_handler_single_step()

                if debug_action():
                    self.debugger_active = True
                else:
                    self.debugger_active = False

            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId, debug_event.dwThreadId, continue_status)
        else:
            self.debugger_active = False

    def detach(self):

        if kernel32.DebugActiveProcessStop(self.pid):
            print("Finished debugging. Exiting...")
            return True
        else:
            print(f"[*] There was an error... {GetLastError()}")
            return False

    def open_thread(self, thread_id):

        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread is not None:
            return h_thread
        else:
            print("[*] Could not obtain a valid thread handle.")
            return False

    def enumerate_threads(self):

        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(
            TH32CS_SNAPTHREAD, self.pid)

        if snapshot is not None:

            # You have to set the size of the struct
            # or the call will fail
            thread_entry.dwSize = sizeof(thread_entry)

            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == self.pid:
                    thread_list.append(thread_entry.th32ThreadID)

                success = kernel32.Thread32Next(snapshot, byref(thread_entry))

            # No need to explain this call, it closes handles
            # so that we don't leak them.
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False

    def get_thread_context(self, thread_id=None, h_thread=None):

        context = CONTEXT64()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        # Obtain a handle to the thread
        if h_thread is None:
            self.h_thread = self.open_thread(thread_id)

        # kernel32.SuspendThread(self.h_thread)
        # print('SuspendThread',GetLastError())

        if kernel32.GetThreadContext(self.h_thread, byref(context)):
            return context
        else:
            return False

    def read_process_memory(self, address, length):

        data = ""
        read_buf = create_string_buffer(length)
        count = c_ulong(0)

        kernel32.ReadProcessMemory(self.h_process, c_ulonglong(
            address), read_buf, 5, byref(count))
        data = read_buf.raw

        return data

    def write_process_memory(self, address, data):

        count = c_ulong(0)
        length = len(data)
        c_data = c_char_p(data)

        if not kernel32.WriteProcessMemory(self.h_process, c_ulonglong(address), c_data, length, byref(count)):
            return False
        else:
            return True

    def bp_set(self, address):
        if address not in self.breakpoints:

            # store the original byte
            old_protect = c_ulong(0)
            kernel32.VirtualProtectEx(self.h_process, c_ulonglong(
                address), 1, PAGE_EXECUTE_READWRITE, byref(old_protect))

            original_byte = self.read_process_memory(address, 1)
            if original_byte != False:

                # write the INT3 opcode
                if self.write_process_memory(address, b"\xCC"):

                    # register the breakpoint in our internal list
                    self.breakpoints[address] = (original_byte)
                    return True
            else:
                return False

    def exception_handler_breakpoint(self):
        # check if the breakpoint is one that we set
        if self.exception_address not in self.breakpoints:

            # if it is the first Windows driven breakpoint
            # then let's just continue on
            if self.first_breakpoint == True:
                self.first_breakpoint = False
                print("    > Hit the first breakpoint.")
            else:
                print("    > Hit the unknow breakpoint.")
                return DBG_CONTINUE

        else:
            print("    > Hit user defined breakpoint.")
            # this is where we handle the breakpoints we set
            # first put the original byte back
            self.write_process_memory(
                self.exception_address, self.breakpoints[self.exception_address])
            del self.breakpoints[self.exception_address]
            
            # obtain a fresh context record, reset EIP back to the
            # original byte and then set the thread's context record
            # with the new EIP value
            self.context = self.get_thread_context(h_thread=self.h_thread)
            self.context.Rip -= 1

            kernel32.SetThreadContext(self.h_thread, byref(self.context))

        continue_status = DBG_CONTINUE
        return continue_status

    def func_resolve(self, dll, function):
        kernel32.GetModuleHandleA.restype = c_ulonglong
        handle = kernel32.GetModuleHandleA(dll)

        kernel32.GetProcAddress.restype = c_ulonglong
        address = kernel32.GetProcAddress(c_ulonglong(handle), function)

        kernel32.CloseHandle(c_ulonglong(handle))

        return address

    def bp_set_hw(self, address, length, condition):

        # Check for a valid length value
        if length not in (1, 2, 4):
            return False
        else:
            length -= 1

        # Check for a valid condition
        if condition not in (HW_ACCESS, HW_EXECUTE, HW_WRITE):
            return False

        # Check for available slots
        if 0 not in self.hardware_breakpoints:
            available = 0
        elif 1 not in self.hardware_breakpoints:
            available = 1
        elif 2 not in self.hardware_breakpoints:
            available = 2
        elif 3 not in self.hardware_breakpoints:
            available = 3
        else:
            return False

        # We want to set the debug register in every thread
        for thread_id in self.enumerate_threads():
            context = self.get_thread_context(thread_id=thread_id)

            # Enable the appropriate flag in the DR7
            # register to set the breakpoint
            context.Dr7 |= 1 << (available * 2)

            # Save the address of the breakpoint in the
            # free register that we found
            if available == 0:
                context.Dr0 = address
            elif available == 1:
                context.Dr1 = address
            elif available == 2:
                context.Dr2 = address
            elif available == 3:
                context.Dr3 = address

            # Set the breakpoint condition
            context.Dr7 |= condition << ((available * 4) + 16)

            # Set the length
            context.Dr7 |= length << ((available * 4) + 18)

            # Set this threads context with the debug registers
            # set
            h_thread = self.open_thread(thread_id)
            kernel32.SetThreadContext(h_thread, byref(context))

        # update the internal hardware breakpoint array at the used slot index.
        self.hardware_breakpoints[available] = (address, length, condition)

        return True

    def exception_handler_single_step(self):
        # Comment from PyDbg:
        # determine if this single step event occured in reaction to a hardware breakpoint and grab the hit breakpoint.
        # according to the Intel docs, we should be able to check for the BS flag in Dr6. but it appears that windows
        # isn't properly propogating that flag down to us.
        if self.context.Dr6 & 0x1 and 0 in self.hardware_breakpoints:
            slot = 0
        elif self.context.Dr6 & 0x2 and 1 in self.hardware_breakpoints:
            slot = 0
        elif self.context.Dr6 & 0x4 and 2 in self.hardware_breakpoints:
            slot = 0
        elif self.context.Dr6 & 0x8 and 3 in self.hardware_breakpoints:
            slot = 0
        else:
            # This wasn't an INT1 generated by a hw breakpoint
            continue_status = DBG_EXCEPTION_NOT_HANDLED

        # Now let's remove the breakpoint from the list
        if self.bp_del_hw(slot):
            continue_status = DBG_CONTINUE

        print("    > Hardware breakpoint removed.")
        return continue_status

    def bp_del_hw(self, slot):

        # Disable the breakpoint for all active threads
        for thread_id in self.enumerate_threads():

            context = self.get_thread_context(thread_id=thread_id)

            # Reset the flags to remove the breakpoint
            context.Dr7 &= ~(1 << (slot * 2))

            # Zero out the address
            if slot == 0:
                context.Dr0 = 0x00000000
            elif slot == 1:
                context.Dr1 = 0x00000000
            elif slot == 2:
                context.Dr2 = 0x00000000
            elif slot == 3:
                context.Dr3 = 0x00000000

            # Remove the condition flag
            context.Dr7 &= ~(3 << ((slot * 4) + 16))

            # Remove the length flag
            context.Dr7 &= ~(3 << ((slot * 4) + 18))

            # Reset the thread's context with the breakpoint removed
            h_thread = self.open_thread(thread_id)
            kernel32.SetThreadContext(h_thread, byref(context))

        # remove the breakpoint from the internal list.
        del self.hardware_breakpoints[slot]

        return True

    # TODO: test
    def bp_set_mem(self, address, size):

        # mbi = MEMORY_BASIC_INFORMATION()
        mbi = MEMORY_BASIC_INFORMATION64()

        # Attempt to discover the base address of the memory page
        if kernel32.VirtualQueryEx(self.h_process, c_ulonglong(address), byref(mbi), sizeof(mbi)) < sizeof(mbi):
            return False

        current_page = mbi.BaseAddress

        # We will set the permissions on all pages that are
        # affected by our memory breakpoint.
        while current_page <= address + size:

            # Add the page to the list, this will
            # differentiate our guarded pages from those
            # that were set by the OS or the debuggee process
            self.guarded_pages.append(current_page)

            old_protection = c_ulong(0)
            if not kernel32.VirtualProtectEx(self.h_process, c_ulonglong(current_page), size, mbi.Protect | PAGE_GUARD, byref(old_protection)):
                return False

            # Increase our range by the size of the
            # default system memory page size
            current_page += self.page_size

        # Add the memory breakpoint to our global list
        self.memory_breakpoints[address] = (address, size, mbi)

        return True
