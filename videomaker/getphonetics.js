// location.href="https://cn.bing.com/search?q=define+mass"

words = ["angel", "anger", "angry", "angle"];

phonetic = new Array(words.length);
res=null;
ccc=window.copy


preUrl = "https://cn.bing.com/dict/search?q=";
promisesArray = words.map(w=>fetch(preUrl + w).then(resp=>resp.text()).then(html=>html.match(/UK&#160;(\[.*\]) <\/div>/)?.[1]))
p2 = Promise.all(promisesArray).then((values)=>{
    // console.log(values);
    phonetic = values;
    console.log(phonetic);
    
    res = phonetic.map(it=>it && it.replaceAll(/&#(\d+);/g, (a,b)=>String.fromCharCode(b)));
    console.log(res);
    ccc(res.join('\n'));
    
}
)

// copy(res.join('\n'))
console.log('start')
// ======================================

// fetch("https://cn.bing.com/search?q=define+mas").then(a, b);
// function a(response) {
//     response.text()
//         .then(json=>console.log(json))
//         .catch(err=>console.log('Request Failed', err));
// }
// function b(response) {
//     console.log('rejected')
// }

// =======================

// a= await fetch('https://cn.bing.com/search?q=define+mass');
// a= await fetch('https://cn.bing.com/dict/search?q=mass');
// b= await a.text();
// b.match(/\?id=ODT\.(.*)&/)[1]
// b.match(/UK&#160;(\[.*\]) <\/div>/)[1]
// 'UK&#160;[m&#230;s]'.replaceAll(/&#(\d+);/g,(a,b)=>String.fromCharCode(b))
