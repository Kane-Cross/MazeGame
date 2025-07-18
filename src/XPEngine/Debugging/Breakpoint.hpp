#pragma once

#ifdef DEBUG
namespace XPE{
    inline void Breakpoint(){}
}
#else
#include <iostream>
namespace XPE{
    inline void Breakpoint(){
        std::cout << "[BREAKPOINT] Press enter to continue: " << std::flush;
        char *buffer;
        size_t  n = 1;
        buffer = (char*)malloc(n);
        getline(&buffer, &n, stdin);
        free(buffer);
    }
}
#endif