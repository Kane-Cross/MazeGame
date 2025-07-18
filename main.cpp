#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>

#include "g.hpp"
#include "bin folder/k.hpp"

int main(int argc, const char* argv[]){
<<<<<<< HEAD
    SDL_Init(SDL_INIT_EVERYTHING);
    TTF_Init();
    IMG_Init(IMG_INIT_PNG);
    Mix_Init(MIX_INIT_MP3);







    SDL_Quit();
    TTF_Quit();
    IMG_Quit();
    Mix_Quit();
=======
    log("Test message");
>>>>>>> 8cbdbc6 (Fixed threaded linking and completed dependency checks)
    return 0;
}