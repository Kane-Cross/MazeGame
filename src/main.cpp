#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_mixer.h>

int main(int argc, const char* argv[]){
    SDL_Init(SDL_INIT_EVERYTHING);
    TTF_Init();
    IMG_Init(IMG_INIT_PNG);
    Mix_Init(MIX_INIT_MP3);

    //Some code here

    Mix_Quit();
    IMG_Quit();
    TTF_Quit();
    SDL_Quit();
    return 0;
}