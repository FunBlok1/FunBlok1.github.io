# FunBlok GitHub Pages Multiplayer (Beta)

Your FunBlok website is hosted by GitHub Pages. The multiplayer feature uses Supabase Realtime so players can join the same room without running a server on a home PC.

## One-time setup

1. Open https://supabase.com/dashboard and create a free project.
2. In the project, open **Project Settings → API** (or **Connect**) and copy the Project URL and the **publishable** key (or legacy **anon** key). Never use a service-role or secret key in the website.
3. Open your published FunBlok site and go to **Studio → Online Multiplayer Studio**.
4. Paste the URL and public key, choose a display name, and press **Save connection**.
5. On each device, use the same URL, public key and room code, then press **Create / Join room**.
6. Move with WASD / arrow keys, or use the on-screen direction buttons. Click the world or press **Place shared block** to broadcast a block to others in the room.

## Important limitations

- This is an early 2D multiplayer proof-of-concept added to the existing 3D Studio. It does not yet synchronise the existing 3D Studio's actual parts, avatar physics, game scripts, accounts, or saved worlds.
- Players and blocks are currently live room broadcasts/presence. Blocks are not permanently saved in a database and can disappear when the room empties.
- The room code is not private authentication. Anyone with the project URL/key and room code may join. Do not store private information in rooms.
- Use only the Supabase publishable/anon key in browser code. Never publish a service-role or secret key.
- Supabase free-plan quotas and pauses/limits may apply.
- GitHub Pages deploys the website automatically after the commit, but it may take a few minutes for the public page to refresh.

## Website repository

https://github.com/FunBlok1/FunBlok1.github.io

## How to remove saved settings from a browser

Clear this site's local storage, or remove fb_mp_supabase_url, fb_mp_supabase_key, and fb_mp_name from localStorage in browser developer tools.
