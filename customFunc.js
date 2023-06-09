function convertTime(sec) {
    var hours = Math.floor(sec/3600);
    (hours >= 1) ? sec = sec - (hours*3600) : hours = '00';
    var min = Math.floor(sec/60);
    (min >= 1) ? sec = sec - (min*60) : min = '00';
    (sec < 1) ? sec='00' : void 0;

    (min.toString().length == 1) ? min = '0'+min : void 0;    
    (sec.toString().length == 1) ? sec = '0'+sec : void 0;    

    return hours+':'+min+':'+sec;
}


const data = [
    {'url':'http://localhost:4000/','v':'vv'},
    {'url':'http://localhost:4000/about','v':'vvv'},
    {'url':'https://localhost:4000/','v':'vvps'}

]

filter_data = data.filter(el=>{
   if(el.url !=='http://localhost:4000/'){
    return el
   }
})
console.log(filter_data)

let com = [{
    "q": {
        "name": "q",
        "value": "",
        "tag": "INPUT"
    },
    "undefined": {
        "value": "https://stackoverflow.com/a/74485156/19406553",
        "tag": "INPUT"
    },
    "post-text": {
        "name": "post-text",
        "value": "ou can store any data in a hash table format in browser memory and then access it any time. I'm not sure if we can access localStorage from the content script (it was blocked before), try to do it by yourself. Here's how to do it through you background page (I pass data from content script to background page first, then save it in localStorage):",
        "tag": "TEXTAREA"
    },
    "author": {
        "name": "author",
        "value": "",
        "tag": "INPUT"
    },
    "feed-url": {
        "name": "feed-url",
        "value": "https://stackoverflow.com/feeds/question/20019958",
        "tag": "INPUT"
    }
}]

com.forEach(el => {
    for(var propName in el) {
        console.log()
    }
});


var datas = [
    {
        "comment": 0,
        "keyword": "",
        "pages": 5,
        "sec": 153,
        "video": 4,
        "video_url": [
            "https://www.jiocinema.com/sports/gt-vs-csk/3715059",
            "https://www.jiocinema.com/sports/csk-vs-mi-highlights/3741401",
            "https://www.jiocinema.com/sports/csk-vs-mi-highlights/3741401",
            "https://www.jiocinema.com/sports/csk-vs-mi-highlights/3741401"
        ]
    },
    {
        "comment": 0,
        "keyword": "AI",
        "pages": 11,
        "sec": 174,
        "video": 0,
        "video_url": 0
    },
    {
        "comment": 0,
        "keyword": "Achievement",
        "pages": 4,
        "sec": 297,
        "video": 4,
        "video_url": [
            "https://www.youtube.com/watch?v=zls4a7I_qaM",
            "https://www.youtube.com/watch?v=zls4a7I_qaM",
            "https://www.youtube.com/watch?v=zls4a7I_qaM",
            "https://www.youtube.com/watch?v=zls4a7I_qaM"
        ]
    },
    {
        "comment": 0,
        "keyword": "Algorithms",
        "pages": 4,
        "sec": 945,
        "video": 0,
        "video_url": 0
    },
    {
        "comment": 0,
        "keyword": "AndroidDevelopment",
        "pages": 4,
        "sec": 945,
        "video": 0,
        "video_url": 0
    },
    {
        "comment": 0,
        "keyword": "Angular",
        "pages": 11,
        "sec": 174,
        "video": 0,
        "video_url": 0
    },
   
]
const percentile = (arr, val) => {
    let count = 0;
    arr.forEach(v => {
      if (v < val) {
        count++;
      } else if (v == val) {
        count += 0.5;
      }
    });
    return 100 * count / arr.length;
  }
var value = []
datas.forEach(element => {
    value.push(element.sec)
});





