// scrsaver.cpp : Defines the entry point for the application.
//

#include "stdafx.h"

#include <windows.h>
#include <stdlib.h>
#include <scrnsave.h>  // SCRNSAVE.LIB的头文件
#include "resource.h"

//LRESULT WINAPI ScreenSaveProc (HWND,UINT,WPARAM,LPARAM);
//BOOL WINAPI ScreenSaveConfigureDialog (HWND,UINT,WPARAM,LPARAM);
//BOOL WINAPI RegisterDialogClasses(HINSTANCE);

//定义全局变量
char szIniFileName[]="control.ini";
//屏幕保护程序配置数据存放在control.ini文件
char szSection[32];
//屏幕保护程序配置数据在control.ini文件位置区名称
char szEntry[]="Slide Text:";
char szDaxiao[]="Da Xiao:";
char szSudu[]="Su du:";
char szZColor[]="Zi Ti Yanse:";
char szBJColor[]="BeiJingYanse:";

//屏幕保护程序配置数据项名称
char SlideText[256];
char daxiao[32];
char sudu[32];
char zcolor[32];
char bjcolor[32];

//屏幕保护程序配置数据，这里是文本内容


BOOL WINAPI AboutDialog (HWND hWnd,UINT message,WPARAM wParam, LPARAM lParam);
COLORREF atocolor(char* str) {
	if(str==NULL) return RGB(0,0,0);
	char rgb[3] = {0};
	int colorpos[3] = {0};
	char tempcolor[4];
	memset(tempcolor,0,4);
	int j=0;
	for(int i=0; i<strlen(str)&&j<3; i++) {
		if(str[i]==',') {
			colorpos[j]=i;
			j++;
		}
	}
	colorpos[j]=strlen(str);
	j++;

	int k=0;
	for(i=0; i<j && i<3; i++) {
		memset(tempcolor, 0, 4);
		memcpy( tempcolor, str+k, colorpos[i]-k);
		rgb[i]=atoi(tempcolor);
		k=colorpos[i]+1;
	}

	return RGB(rgb[0], rgb[1], rgb[2]);
}

LRESULT WINAPI ScreenSaverProc (HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	HDC hDC;
	RECT rc;
	static int xpos, ypos;//文本的横坐标
	static int dx;//text size.
	static char SlideText[256]="欢迎使用屏幕保护程序!";
	static UINT timerID;//定时器
	static HFONT hfontnew;
	static COLORREF zicolor, beijcolor;
	static HBRUSH hbrush;
	switch (message)
	{
	case WM_CREATE:
		{
		//文件位置区名称szSection赋值为资源 idsAPPName。其中hMainInstance为
		//SCRNSAVE.LIB定义的屏幕保护程序实例句柄
		LoadString(hMainInstance,idsAPPName, szSection,sizeof(szSection));
		strcpy(SlideText,"欢迎使用屏幕保护程序!");
		//读control.ini文件中[Screen Saver.MySaver] 区的配置数据到SlideText
		GetPrivateProfileString(szSection,
			szEntry, SlideText,SlideText, sizeof(SlideText),szIniFileName);

		strcpy(daxiao, "32");
		GetPrivateProfileString(szSection,
			szDaxiao,daxiao,daxiao,sizeof(daxiao),szIniFileName);
		dx = atoi(daxiao);
		if(dx<0) dx=32;
		if(dx>90) dx=90;

		strcpy(sudu,"250");
		GetPrivateProfileString(szSection,
			szSudu,sudu,sudu,sizeof(sudu),szIniFileName);
		int sd = atoi(sudu);
		if(sd<0) sd=25;
		if(sd>1000) sd=1000;

		strcpy(zcolor,"255,0,0");
		GetPrivateProfileString(szSection,
			szZColor,zcolor,zcolor,sizeof(zcolor),szIniFileName);
		zicolor=atocolor(zcolor);

		strcpy(bjcolor,"0,0,255");
		GetPrivateProfileString(szSection,
			szBJColor,bjcolor,bjcolor,sizeof(bjcolor),szIniFileName);
		beijcolor=atocolor(bjcolor);
		hbrush = CreateSolidBrush(beijcolor);
		//取位图
		// hBmp=LoadBitmap(hMainInstance,MAKEINTRESOURCE(IDB_BITMAP1));
		//设置字体
		hfontnew = CreateFontA(dx,0,0,0,700,0,0,0,134,0,0,0,0,"楷体_GB2312");
		timerID=SetTimer(hWnd,1,sd,NULL);
		xpos=GetSystemMetrics(SM_CXSCREEN);
		ypos=dx+(rand()%(GetSystemMetrics(SM_CYSCREEN)-2*dx));
		}
		break;
		
	case WM_ERASEBKGND:
		//空操作，交由DefScreenSaverProc处理
		break;
	case WM_TIMER:
		hDC=GetDC(hWnd);
		//清屏
		SetRect(&rc,0,0,GetSystemMetrics(SM_CXSCREEN),
			GetSystemMetrics(SM_CYSCREEN));
		FillRect(hDC,&rc,(HBRUSH)hbrush);
		//输出文本
		SelectObject(hDC,hfontnew);
		SetTextColor(hDC, zicolor);
		SetBkColor(hDC,beijcolor);
		TextOut(hDC,xpos,ypos,
			SlideText,strlen(SlideText));
		//移动文本的横坐标
		xpos=(xpos-10);
		if(xpos <= -GetSystemMetrics(SM_CXSCREEN)) {
			xpos = GetSystemMetrics(SM_CXSCREEN);
			ypos=dx+(rand()%(GetSystemMetrics(SM_CYSCREEN)-2*dx));
		}
		ReleaseDC(hWnd,hDC);
		break;
		
	case WM_DESTROY:
		KillTimer(hWnd,timerID);//删除定时器
		PostQuitMessage (0);
		return 0;
	}
	return DefScreenSaverProc (hWnd,message,wParam,lParam);
}

BOOL WINAPI ScreenSaverConfigureDialog (HWND hWnd,UINT message,WPARAM wParam, LPARAM lParam)
{ 
	switch (message)
	{
	case WM_INITDIALOG:
		LoadString(hMainInstance,idsAPPName,
			szSection,sizeof(szSection));
		strcpy(SlideText,"欢迎使用屏幕保护程序!");
		GetPrivateProfileString(szSection,
			szEntry,SlideText,
			SlideText,sizeof(SlideText),szIniFileName);
		SetDlgItemText(hWnd,IDC_EDIT,SlideText);
		SetFocus(GetDlgItem(hWnd,IDC_EDIT));

		strcpy(daxiao, "32");
		GetPrivateProfileString(szSection,
			szDaxiao,daxiao,daxiao,sizeof(daxiao),szIniFileName);
		SetDlgItemText(hWnd,IDC_EDIT_DAXIAO,daxiao);

		strcpy(sudu,"250");
		GetPrivateProfileString(szSection,
			szSudu,sudu,sudu,sizeof(sudu),szIniFileName);
		SetDlgItemText(hWnd,IDC_EDIT_SUDU,sudu);

		strcpy(zcolor,"255,0,0");
		GetPrivateProfileString(szSection,
			szZColor,zcolor,zcolor,sizeof(zcolor),szIniFileName);
		SetDlgItemText(hWnd,IDC_EDIT_WENZICOLOR,zcolor);

		strcpy(bjcolor,"0,0,255");
		GetPrivateProfileString(szSection,
			szBJColor,bjcolor,bjcolor,sizeof(bjcolor),szIniFileName);
		SetDlgItemText(hWnd,IDC_EDIT_BJCOLOR, bjcolor);
		return FALSE;
		
	case WM_COMMAND:
		switch(wParam)
		{
		case IDOK:
			//取EDIT控件文本数据并写入control.ini文件
			GetDlgItemText(hWnd,IDC_EDIT,
				SlideText,sizeof(SlideText));
			GetDlgItemText(hWnd,IDC_EDIT_DAXIAO, daxiao, sizeof(daxiao));
			GetDlgItemText(hWnd,IDC_EDIT_SUDU, sudu, sizeof(sudu));
			GetDlgItemText(hWnd,IDC_EDIT_WENZICOLOR, zcolor, sizeof(zcolor));
			GetDlgItemText(hWnd,IDC_EDIT_BJCOLOR, bjcolor, sizeof(bjcolor));

			WritePrivateProfileString(szSection,
				szEntry,SlideText,szIniFileName);
			WritePrivateProfileString(szSection,
				szDaxiao,daxiao,szIniFileName);
			WritePrivateProfileString(szSection,
				szSudu,sudu,szIniFileName);
			WritePrivateProfileString(szSection,
				szZColor,zcolor,szIniFileName);
			WritePrivateProfileString(szSection,
				szBJColor,bjcolor,szIniFileName);
			
			EndDialog(hWnd,TRUE);
			return TRUE;
			
		case IDCANCEL:
			EndDialog(hWnd,FALSE);
			return TRUE;
			
		case IDABOUT:
			//调用ABOUT对话框
			DialogBox(hMainInstance,
				MAKEINTRESOURCE(DLG_ABOUT),
				hWnd,AboutDialog);
			return TRUE;
		}
		break;
	}
	return FALSE;
}


BOOL WINAPI RegisterDialogClasses (HANDLE hInst)
{//一般不需要，仅返回TRUE
	return TRUE;
}

BOOL WINAPI AboutDialog
(HWND hWnd,UINT message,WPARAM wParam,
 LPARAM lParam)
{ 
	switch (message)
	{
	case WM_INITDIALOG:
		return TRUE;
		
	case WM_COMMAND:
		switch(wParam)
		{
		case IDOK:
			EndDialog(hWnd,TRUE);
			return TRUE;
		}
		break;
	}
	return FALSE;
}




