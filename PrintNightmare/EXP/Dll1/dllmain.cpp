// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include <cstdint>
#include <fstream>
#include <string>



int Injection()
{
	char cmd[] = "cmd.exe";
	uint32_t pid = GetCurrentProcessId();
	std::ofstream myfile;
	std::string filename;
	std::string path = "c:\\windows\\tasks\\";
	std::string file_ext = ".txt";
	filename = path + std::to_string(pid) + file_ext;
	myfile.open(filename);

	//myfile << "Process: " + ProcessIdToName(pid) + "\n";
	myfile << "PID: " + std::to_string(pid) + "\n";
	//myfile << "Injected as: " + GetProcessUsername(NULL) + "\n";
	myfile << "############################################\n";
	myfile.close();
	//WinExec(cmd, SW_SHOWNORMAL);
	return 0;

}
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
		Injection();
		break;
    case DLL_THREAD_ATTACH:
		break;
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

