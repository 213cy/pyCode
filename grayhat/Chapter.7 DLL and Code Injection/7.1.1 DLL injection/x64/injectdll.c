#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif

#include <stdio.h>
#include <windows.h>
// #include <tchar.h>
// #include <stdlib.h>

void WriteLocalTimeToBuffer(char *buf)
{
    SYSTEMTIME systemTime;
    // Get the current local time
    GetLocalTime(&systemTime);
    // Print the current local time in a formatted way
    sprintf(buf, "[%04d-%02d-%02d %02d:%02d:%02d.%03d]",
            systemTime.wYear,
            systemTime.wMonth,
            systemTime.wDay,
            systemTime.wHour,
            systemTime.wMinute,
            systemTime.wSecond,
            systemTime.wMilliseconds);
}

INT APIENTRY DllMain(HMODULE hDLL, DWORD Reason, LPVOID Reserved)
{
    /* open file */
    FILE *file;

    wchar_t dllFileName[MAX_PATH];
    wchar_t exeFileName[MAX_PATH];

    char logMessage[256];
    char timeMessage[256];

    GetModuleFileName(hDLL, dllFileName, sizeof(dllFileName));

    wchar_t *pwc = wcsrchr(dllFileName, L'\\');
    *pwc = L'\0';
    wcscat(dllFileName, L"\\log.txt");
    // printf("filename : %ls\n", dllFileName);

    _wfopen_s(&file, dllFileName, L"a+");

    // -----------------

    WriteLocalTimeToBuffer(timeMessage);
    HMODULE hModule;
    HMODULE hSelf;
    HMODULE hKernel32;
    DWORD dwFlags;

    switch (Reason)
    {
    case DLL_PROCESS_ATTACH:
        hModule = GetModuleHandle(NULL); // NULL means the current process
        GetModuleFileName(hModule, exeFileName, sizeof(exeFileName) / sizeof(TCHAR));
        int ret = wcstombs(logMessage, exeFileName, sizeof(logMessage));

        // Get the module handle from the function address

        dwFlags = GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT;
        GetModuleHandleEx(dwFlags, (LPCTSTR)DllMain, &hSelf);
        // GetModuleHandleEx(dwFlags, DllMain, &hSelf);

        hKernel32 = GetModuleHandle(L"kernel32.dll");
        sprintf(logMessage + ret, "\nhDLL (%d)= %#x  hKernel32 = %#x \n", hDLL - hSelf, hDLL, hKernel32);

        strcat(logMessage, timeMessage);
        fprintf(file, strcat(logMessage, " >>>    DLL process attach\n"));

        MessageBox(NULL, dllFileName, L"logFileName", MB_ICONINFORMATION | MB_OK);
        break;
    case DLL_PROCESS_DETACH:
        fprintf(file, strcat(timeMessage, "    <<< DLL process detach\n"));
        break;
    case DLL_THREAD_ATTACH:
        fprintf(file, strcat(timeMessage, "        >>>    DLL thread attach\n"));
        break;
    case DLL_THREAD_DETACH:
        fprintf(file, strcat(timeMessage, "           <<< DLL thread detach\n"));
        break;
    }

    /* close file */
    fclose(file);

    return TRUE;
}
