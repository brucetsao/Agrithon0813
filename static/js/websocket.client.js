/**
 * Created by hatsukiotowa on 2016/8/12.
 */

//如果 data.tab 有資料
if (data.tab) {
    //因為 data.tab 抓到的資料是 #1, #2, #3... 這樣的值，為了只取數字，所以用 substring 去做截斷
    for(var x = 1; x &lt; data.tab.substring(1,2); x ++) {
        if(x == 1){
            $("#testdiv").css("display", "block");
          }
    };
};