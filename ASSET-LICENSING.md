# FunBlok asset and third-party licence audit

Last reviewed: 11 November 2026

This file records the external assets and libraries found in the current GitHub Pages app. It is an audit of the repository contents, not a legal guarantee that every historical contribution or future upload is cleared.

## FunBlok-owned presentation

The current app is delivered from `index.html`. In the repository tree reviewed for this audit, there are no separate image, audio, video, 3D model, texture, or font asset files. The page does not contain ordinary external image URLs or CSS background-image URLs.

The 3D Studio primitives are generated in JavaScript at runtime. The interface uses CSS, system fonts, and Unicode emoji glyphs supplied by the visitor's operating system/browser. The Studio shape previously labelled "Wedge" is presented to players as "Ramp".

Keep future uploads original, commissioned with written rights, or under a licence that explicitly permits the intended use. Record the creator, source URL, licence, and any required attribution for each third-party asset before adding it.

## Third-party software currently loaded

These dependencies are not public-domain or copyright-free. They are third-party software under their own permissive MIT licences, and their copyright/licence notices must be respected.

| Dependency | Current use | Licence / source |
| --- | --- | --- |
| Three.js r128 | 3D rendering | MIT — https://cdnjs.com/libraries/three.js/r128 and https://github.com/mrdoob/three.js |
| Three.js OrbitControls (r128 examples) | Studio camera controls | MIT — part of the Three.js project; https://github.com/mrdoob/three.js |
| Supabase JavaScript client v2 | Hosted database and realtime client | MIT — https://github.com/supabase/supabase-js |

The app currently loads these libraries from public CDNs. Do not remove or overwrite their upstream copyright and licence notices if the libraries are later vendored into this repository. Keep the dependency version and licence recorded here up to date.

## Branding and content policy

- FunBlok must use its own name, logo, visual identity, UI artwork, sounds, character designs, game worlds, and item designs.
- Do not add Roblox logos, trademarks, proprietary client binaries, ripped textures/models/audio, copied website source, or assets downloaded from an archive unless a clear licence or written permission allows that exact reuse.
- A genre convention or broad design idea can be used as inspiration; do not copy distinctive artwork, text, layouts, or source code.
- Do not describe the whole project as "copyright-free". Original work is protected by copyright automatically unless its rights holder applies a suitable licence or dedication. Third-party dependencies retain their own rights and licence terms.
- Before publishing any user-created content, require the uploader to confirm they have the necessary rights and provide a reporting/removal process.

## Re-audit checklist for new releases

- [ ] Check every new image, sound, video, model, texture, font, and script dependency.
- [ ] Save the source and exact licence for each third-party asset.
- [ ] Keep required attribution and notices.
- [ ] Remove any unlicensed copied content.
- [ ] Re-run the repository's automatic tests and inspect the published site.
