<script>
    //wordscloud
    // Function to filter data based on the selected time period
    const tonality_and_emotion_array = (filtered_data) => {
      const seenComments = new Set();
      const filteredComments = [];
      const tonality = [];
      const emotion = [];

      for (const entry of filtered_data) {
        if ('comment' in entry) {
          const commentList = entry['comment'];
          if (Array.isArray(commentList)) { // Check if commentList is an array
            for (const commentEntry of commentList) {
              if ('comment' in commentEntry) {
                const commentText = commentEntry['comment'];
                if (!seenComments.has(commentText)) {
                  seenComments.add(commentText);
                  filteredComments.push(commentEntry);
                  if ('tonality' in commentEntry) {
                    tonality.push(commentEntry['tonality']);
                  }
                  if ('emotion' in commentEntry) {
                    emotion.push(commentEntry['emotion']);
                  }
                }
              }
            }
          }
        }
      }

      // Calculate unique values and corresponding percentiles for tonality
      const uniqueValuesTon = [];
      const uniquePercentilesTon = [];

      for (const value of tonality) {
        if (!uniqueValuesTon.includes(value)) {
          uniqueValuesTon.push(value);
          const percentile = calculatePercentile(tonality, value);
          uniquePercentilesTon.push(percentile);
        }
      }

      // Calculate unique labels and corresponding percentiles for emotion
      const uniqueValEmo = [];
      const uniquePercentilesEmo = [];

      for (const label of emotion) {
        if (!uniqueValEmo.includes(label)) {
          uniqueValEmo.push(label);
          const percentile = calculatePercentile(emotion, label);
          uniquePercentilesEmo.push(percentile);
        }
      }

      // Define a function to calculate percentiles (you need to implement this function)
      function calculatePercentile(valueList, value) {
        const count = valueList.reduce((accumulator, currentValue) => {
          return currentValue === value ? accumulator + 1 : accumulator;
        }, 0);

        return (count / valueList.length) * 100;
      }
      var tonEmo_data = []
      if (filteredComments.length > 0) { tonEmo_data.push({ 'ton': [uniqueValuesTon, uniquePercentilesTon], 'emo': [uniqueValEmo, uniquePercentilesEmo], 'tot_comments': filteredComments.length }) }
      else { tonEmo_data.push({ 'ton': [['Tonality Not Found'], [[100]]], 'emo': [['Emotion Not Found'], [[100]]], 'tot_comments': 0 }) }
      return tonEmo_data
    }






    var keywords = {{ wordcloud_data| tojson}}

    var keyword_array = keywords.filter(el => { if (el.keyword !== 'localhost:4000') { return el } })


    const count_datas = {{ count_data | tojson}}
    const count_data_parse = JSON.parse(count_datas)

    const duration = document.getElementById("duration");
    const screettime = document.getElementById("sc-time");
    duration.textContent = hourMin(count_data_parse[1]);
    screettime.textContent = hourMin(count_data_parse[1]);

    const timePeriodDropdown = document.getElementById('timePeriodDropdown');
    const searchForm = document.querySelector('.search-form');

    searchForm.addEventListener('submit', function (e) {
      e.preventDefault(); // Prevent the form from submitting


      const selectedTimePeriod = parseInt(timePeriodDropdown.value);
      selectedDate = selectedTimePeriod
      filered_data = filterDataByTimePeriod(keyword_array, selectedDate)
      let ton_emo_data = tonality_and_emotion_array(filered_data)
      console.log(ton_emo_data)
      console.warn('filter data')
      console.log(filered_data)
      const values = filered_data.map(el => { return el.sec })
      const newData = filered_data.filter(el => { el.percent = percentile(values, el.sec); return el })

      const newlist = []

      newData.forEach(element => { newlist.push([element.keyword, Math.floor(element.percent), element.comment, element.video_url, element.pages, element.sec]) });
      //console.warn(filteredData)
      const uniqueValues = {};
      const filteredData = newlist.filter(item => {
        const value = item[1]; if (!uniqueValues.hasOwnProperty(value)) {
          uniqueValues[value] = true; return true; // Keep the item in the filtered array
        }
        return false; // Remove the duplicate item
      });
      var totPage = 0;
      var totComment = 0;
      var totalSec = 0;
      var totVid = 0


      newlist.forEach(el => {
        totPage += el[4]; totalSec += el[5];
        if (Array.isArray(el[2])) { totComment += el[2].length; }
        if (Array.isArray(el[3])) { totVid += el[3].length; }
      });
      const totalVideo = document.getElementById("totalVideo");
      const pages = document.getElementById("pages");
      const comments = document.getElementById("comments");
      totalVideo.textContent = totVid;
      pages.textContent = count_data_parse[0];
      comments.textContent = count_data_parse[2];

      const restructuredData = restructureArray(newlist);
      createWordCloud(restructuredData);
      createDonutChart(ton_emo_data[0].ton)
      createEmotionDonutChart(ton_emo_data[0].emo)
      



    });

    function hourMin(sec) { let totalSeconds = sec; let hours = Math.floor(totalSeconds / 3600); let minutes = Math.floor((totalSeconds % 3600) / 60); return (hours + " hours " + minutes + ""); }
    let wordWrap = document.getElementById("check");
    // percentile of url duration
    const percentile = (arr, val) => { let count = 0; arr.forEach(v => { if (v < val) { count++; } else if (v == val) { count += 0.5; } }); return 100 * count / arr.length; }
    //


    //demo list
    let list = [["foo", 21, "http://yahoo.com"],];



   
    //tonality and emotion graphs
  

    // Call the async function to create the WordCloud


    // Given array

    function removePrefixAndCom(domain) { return domain.replace(/^(web\.|app\.|app\.|www\.|chat\.)/, '').replace(/\.com$/, ''); }

    // Function to restructure the array
    function restructureArray(data) { const restructuredData = []; for (const item of data) { const domain = removePrefixAndCom(item[0]); restructuredData.push([domain, ...item.slice(1)]); } return restructuredData; }










  </script>

  <script>
    var language_accuracy = {{ language_accurac | tojson}}

    console.log(language_accuracy)
    let lang_acc_data_by_timestamp = language_accuracy[4]
    console.log(lang_acc_data_by_timestamp[0].time.$date)


    // Get references to HTML elements
    const rawData = lang_acc_data_by_timestamp


    // Event listener for form submission
    searchForm.addEventListener('submit', function (e) {
      e.preventDefault(); // Prevent the form from submitting

      // Get the selected time period value
      const selectedTimePeriod = parseInt(timePeriodDropdown.value);

      // Calculate the date threshold based on the selected time period
      const currentDate = new Date();
      let thresholdDate = new Date(currentDate);
      if (selectedTimePeriod !== 1) { thresholdDate.setDate(currentDate.getDate() - selectedTimePeriod); }

      // Filter the rawData based on the timestamp
      filterData = rawData.filter((item) => {const itemTimestamp = new Date(item.time.$date); return itemTimestamp >= thresholdDate;});
      

      // Now, 'filterData' contains the filtered data based on the selected time period
      let grammarCorrect = [];let spellCorrect = [];let fluency = [];let impression = [];

      for (let item of filterData) {
        grammarCorrect.push(100 - item['grammer_mistake_count']);
        console.log(item['grammer_mistake_count']);
        spellCorrect.push(item['spell_mistake_count']);
        fluency.push(item['fluent']);
        impression.push(item['impression']);
      }

      let grammarCorrectAverage = grammarCorrect.reduce((acc, val) => acc + val, 0) / grammarCorrect.length;
      let spellCorrectAverage = spellCorrect.reduce((acc, val) => acc + val, 0) / spellCorrect.length;
      let fluencyAverage = fluency.reduce((acc, val) => acc + val, 0) / fluency.length;
      let impressionAverage = impression.reduce((acc, val) => acc + val, 0) / impression.length;

      let result = [grammarCorrectAverage, spellCorrectAverage, fluencyAverage, impressionAverage, filterData];

      console.warn(filered_data);
      console.warn(result)
      console.log('Selected Time Period:', selectedTimePeriod);
      console.log('Current Date:', currentDate);
      console.log('Threshold Date:', thresholdDate);
      createRadialBarChart(result);
      document.getElementById('gr-correct').textContent = result[0].toFixed(2)
      document.getElementById('sp-correct').textContent = result[1].toFixed(2)
      document.getElementById('fl-correct').textContent = result[2].toFixed(2)
      document.getElementById('rt-correct').textContent = result[3].toFixed(2)
    });









    

    // Call the async function to create the radial bar chart



  </script>

  <script>
    let tonalityChart = document.querySelector(".tonality-chart");
    const data_emo = {{ dataton | tojson}}


    tonality_emotion1 = JSON.parse(data_emo)


    emotion = tonality_emotion1[0].emo
   

    // Call the async function to create the donut chart

  

  </script>

  <script>
    const data_ton = {{ dataton | tojson}}
    console.log(data_ton)
    tonality_emotion = JSON.parse(data_ton)
    console.log(tonality_emotion[0].ton)
    tonality = tonality_emotion[0].ton
    emotion = tonality_emotion[0].emo
  

    // Call the async function to create the donut chart with emotions


  </script>

  <script>
    const screen_time = {{ screenTime | tojson}}
    const screen_time_parse = JSON.parse(screen_time)
    console.log(screen_time_parse)
    const childID = {{ child_id | tojson}}
    console.log(childID)
    

    // Call the async function to create the area chart for screen time
    createScreenTimeAreaChart();


  </script>

  <script>
    const filterDataByTimePeriod = (rawData, selectedTimePeriod) => {
      // Calculate the date threshold based on the selected time period
      const currentDate = new Date();
      let thresholdDate = new Date(currentDate);

      if (selectedTimePeriod !== 1) {
        thresholdDate.setDate(currentDate.getDate() - selectedTimePeriod);
      }

      // Filter the rawData based on the timestamp
      const filterData = rawData.filter((item) => {
        // Split the concatenated timestamps into individual timestamps
        const timestamps = item.timestamp.split(/\s+/);

        // Iterate through each timestamp and check if it's within the selected time period
        for (const timestamp of timestamps) {
          const timestampDate = new Date(timestamp);

          // Check if the timestamp is a valid Date object
          if (!isNaN(timestampDate.getTime()) && timestampDate >= thresholdDate) {
            return true; // Include the item if any timestamp matches the condition
          }
        }

        return false; // Exclude the item if none of the timestamps match the condition
      });

      return filterData;
    }
  
  </script>