
//输入格式判断
function IsDigit(cCheck) 
{ 
	return (('0'<=cCheck) && (cCheck<='9')); 
} 

function IsAlpha(cCheck) 
{ 
	return ((('a'<=cCheck) && (cCheck<='z')) || (('A'<=cCheck) && (cCheck<='Z'))) 
} 

function IsValid() 
{ 
	var struserName = reg.username.value; 
	for (nIndex=0; nIndex<struserName.length; nIndex++) 
	{ 
		cCheck = struserName.charAt(nIndex); 
		if (!(IsDigit(cCheck) || IsAlpha(cCheck))) { 
			return false; 
		} 
	} 
	return true; 
} 

function do_check() 
{ 
	if(reg.username.value=="") { 
		alert("请填写用户名");
		return false; 
	} 
	else if(!IsValid()) { 
		alert("用户名只能使用字母和数字"); 
		return false; 
	} 
	else if(reg.password.value=="") { 
		alert("请填写密码"); 
		return false; 
	} 
	else if(reg.email.value=="") { 
		alert("请填写邮箱"); 
		return false; 
	} 
	else if(reg.password.value != reg.cpassword.value) { 
		alert("两次密码不一致"); 
		return false; 
	} 

	else 
	{ 
		return true; 
	} 
} 

