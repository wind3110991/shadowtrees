var curIndex=0;
var timeInterval=5000;
var arr=new Array();
var arrWeb=new Array();
arr[0]="http://imglf4.ph.126.net/3zhEimItB4RElfHU4NRhiA==/6597791046284502424.jpg";
arr[1]="http://abc.2008php.com/2011_Website_appreciate/2011-10-13/20111013214302.jpg";
arr[2]="http://img.56youxi.com/attachment/103_433_f101f7e70bf15e4.jpg";
arr[3]="http://pic2.duowan.com/news/1210/214228446151/214228538017.jpg";
arrWeb[0]="http://tieba.baidu.com/f?kw=地下乐队&ie=utf-8&fr=wwwt";
arrWeb[1]="http://www.levi.com.cn";
arrWeb[2]="http://tieba.baidu.com/f?kw=科比&ie=utf-8&fr=wwwt";
arrWeb[3]="http://weibo.com/realyuwenle?c=spr_qdhz_bd_baidusmt_weibo_s&nick=余文樂";
setInterval(changeImg,timeInterval);
function changeImg()
{
	var obj=document.getElementById("obj");
	var objWeb=document.getElementById("objWeb");
	if(curIndex==arr.length-1)
	{
		curIndex=0;
	}
	else
	{
		curIndex+=1;
	}
	obj.src=arr[curIndex];
	objWeb.href=arrWeb[curIndex];
}
$(document).ready(changeImg);


