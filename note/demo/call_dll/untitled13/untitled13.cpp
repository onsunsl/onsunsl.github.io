#include "untitled13.h"


//Untitled13::Untitled13()
//{
//}



#include <stdio.h>

#include <Windows.h>

// 如果有调试器，则不会执行这个函数
BOOL bIsBeinDbg = TRUE;

LONG WINAPI UnhandledExcepFilter(PEXCEPTION_POINTERS pExcepPointers)
{
    // EXCEPTION_EXECUTE_HANDLER(1)：表示该异常被处理，从异常处下一条指令继续执行
    // EXCEPTION_CONTINUE_SEARCH(0)：表示异常不能被处理，交给下一个SEH
    // EXCEPTION_CONTINUE_EXECUTION(-1)：表示异常被忽略，从异常处继续执行

    printf("code:%d\n", pExcepPointers->ExceptionRecord->ExceptionCode);
    // TODO 保存dump 操作
    return EXCEPTION_EXECUTE_HANDLER;
}

void new_obj(int i)
{


    LPTOP_LEVEL_EXCEPTION_FILTER t = SetUnhandledExceptionFilter(UnhandledExcepFilter);
//    LPTOP_LEVEL_EXCEPTION_FILTER t = SetUnhandledExceptionFilter(UnhandledExcepFilter);
    char a[2] = {'1', '2'};
    printf("hello c++:%c\n", a[i]);
    printf("hello c++:%d\n", t);
    int b = 0;
    printf("%d", 100/b);
}

void mem_test()
{
    char *str = "hello mem_test\n";
    printf("%s", str);
    str[6] = '0';
}
