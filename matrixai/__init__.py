import simplematrixbotlib as botlib
import os
import sys
from baichat_py import Completion

PREFIX = "!"

USERNAME = os.environ.get("MATRIX_USERNAME", "ai")
SERVER = os.environ.get("MATRIX_SERVER", "https://matrix.projectsegfau.lt")
PASSWORD = os.environ.get("MATRIX_PASSWORD", None)

ENABLE_AI_COMMAND = os.environ.get("ENABLE_AI_COMMAND", True)
ENABLE_IMAGE_COMMAND = os.environ.get("ENABLE_IMAGE_COMMAND", True)

AI_COMMAND_ALIASES = os.environ.get("AI_COMMAND_ALIASES", "ask, ai, gpt").split(", ")
IMAGE_COMMAND_ALIASES = os.environ.get("IMAGE_COMMAND_ALIASES", "img, i").split(", ")

PING_URL = os.environ.get(
    "PING_URL",
    "https://healthchecks.projectsegfau.lt/ping/2f7f2cd3-2a8d-4fff-b5ca-f4d17d47f75b",
)

SYSTEMD_SERVICE_NAME = os.environ.get("SYSTEMD_SERVICE_NAME", "matrixai")

import io

import aiohttp
import asyncio
import os
from langdetect import detect

from enum import Enum
import uuid
import subprocess


class Style(Enum):
    """
    Enumeration class for different styles. Each style has three attributes:
    - styles_id: Identifier for the style.
    - asset: Reference to the asset associated with the style.
    - asset_path: The folder of the asset
    - suffix: Additional descriptor that can be appended to a prompt when using the style.
    """

    IMAGINE_V4_Beta = (30, "Imagine_V3.5", "styles_v1", None)
    V4_CREATIVE = (31, "thumb-64", "styles_v4", None)
    IMAGINE_V3 = (28, "thumbv1_27", "styles_v1", ", 4k, high quality, hdr")
    IMAGINE_V1 = (27, "thumb-63", "styles_v4", None)
    PORTRAIT = (26, "thumb-65", "styles_v4", None)
    REALISTIC = (29, "thumb-66", "styles_v4", None)
    ANIME = (21, "thumb_20", "styles", None)
    ANIME_V2 = (
        28,
        "thumb_37",
        "styles_v1",
        ", anime atmospheric, atmospheric anime, anime character; full body art, digital anime art, beautiful anime art style, anime picture, anime arts, beautiful anime style, digital advanced anime art, anime painting, anime artwork, beautiful anime art, detailed digital anime art, anime epic artwork",
    )
    COSMIC = (
        28,
        "thumb-01",
        "styles_v4",
        ", in cosmic atmosphere, humanitys cosmic future,  space art concept, space landscape, scene in space, cosmic space, beautiful space star planet, background in space, realistic, cinematic, breathtaking view",
    )
    COMIC_V2 = (
        28,
        "thumb_34",
        "styles_v1",
        ", comic book, john romita senior, inspired by Alton Tobey, by Alan Davis, arachnophobia, by Alton Tobey, as a panel of a marvel comic, marvel comic",
    )
    MARBLE = (
        28,
        "thumb-02",
        "styles_v4",
        ", in greek marble style, classical antiquities, ancient greek classical ancient greek art, marble art, realistic, cinematic",
    )
    MINECRAFT = (
        28,
        "thumb-03",
        "styles_v4",
        ", minecraft build, style of minecraft, pixel style, 8 bit, epic, cinematic, screenshot from minecraft, detailed natural lighting, minecraft gameplay, mojang,  minecraft mods, minecraft in real life,  blocky like minecraft",
    )
    DISNEY = (
        28,
        "thumb-04",
        "styles_v4",
        ", disney animation, disney splash art, disney color palette, disney renaissance film, disney pixar movie still, disney art style, disney concept art :: nixri, wonderful compositions, pixar, disney concept artists, 2d character design",
    )
    MACRO_PHOTOGRAPHY = (
        28,
        "thumb-05",
        "styles_v4",
        ", macro photography, award winning macro photography, depth of field, extreme closeup, 8k hd, focused",
    )
    GTA = (
        28,
        "thumb-06",
        "styles_v4",
        ", gta iv art style, gta art,  gta loading screen art, gta chinatowon art style, gta 5 loading screen poster, grand theft auto 5, grand theft auto video game",
    )
    STUDIO_GHIBLI = (
        28,
        "thumb-07",
        "styles_v4",
        ", studio ghibli movie still, ghibli screenshot, joe hisaishi, makoto shinkai, cinematic studio ghibli still, fantasy art landscape, whimsical, dreamlike, anime beautiful peace scene, studio ghibli painting, cinematic",
    )
    DYSTOPIAN = (
        28,
        "thumb-08",
        "styles_v4",
        ", cifi world, cybernetic civilizations, peter gric and dan mumford,   brutalist dark futuristic, dystopian brutalist atmosphere, dark dystopian world, cinematic 8k, end of the world, doomsday",
    )
    STAINED_GLASS = (
        28,
        "thumb-09",
        "styles_v4",
        ", intricate wiccan spectrum, stained glass art, vividly beautiful colors, beautiful stained glass window, colorful image, intricate stained glass triptych, gothic stained glass style, stained glass window!!!",
    )
    PRODUCT_PHOTOGRAPHY = (
        28,
        "thumb-10",
        "styles_v4",
        ", product photo studio lighting,  high detail product photo, product photography, commercial product photography, realistic, light, 8k, award winning product photography, professional closeup",
    )
    PSYCHEDELIC = (
        28,
        "thumb-11",
        "styles_v4",
        ", psychedelic painting, psychedelic dripping colors, colorful detailed projections, android jones and chris dyer, psychedelic vibrant colors, intricate psychedelic patterns, psychedelic visuals, hallucinatory art",
    )
    SURREALISM = (
        28,
        "thumb-12",
        "styles_v4",
        ", salvador dali painting, highly detailed surrealist art, surrealist conceptual art,  masterpiece surrealism, surreal architecture, surrealistic digital artwork, whimsical surrealism, bizarre art",
    )
    GRAFFITI = (
        28,
        "thumb-13",
        "styles_v4",
        ", graffiti background, colorful graffiti, graffiti art style, colorful mural, ravi supa, symbolic mural, juxtapoz, pablo picasso, street art",
    )
    GHOTIC = (
        28,
        "thumb-14",
        "styles_v4",
        ", goth lifestyle, dark goth, grunge, cinematic photography, dramatic dark scenery, dark ambient beautiful",
    )
    RAINBOW = (
        28,
        "thumb-15",
        "styles_v4",
        ", intricate rainbow environment, rainbow bg, from lorax movie, pixar color palette, volumetric rainbow lighting, gorgeous digital painting, 8k cinematic",
    )
    AVATAR = (
        28,
        "thumb-16",
        "styles_v4",
        ", avatar movie, avatar with blue skin, vfx movie, cinematic lighting, utopian jungle, pandora jungle, sci-fi nether world, lost world, pandora fantasy landscape,lush green landscape, high quality render",
    )
    PALETTE_KNIFE = (
        28,
        "thumb-17",
        "styles_v4",
        ", detailed impasto brush strokes,  detail acrylic palette knife, thick impasto technique,  palette knife, vibrant 8k colors",
    )
    CANDYLAND = (
        28,
        "thumb-18",
        "styles_v4",
        ", candy land style,  whimsical fantasy landscape art, japanese pop surrealism, colorfull digital fantasy art, made of candy and lollypops, whimsical and dreamy",
    )
    CLAYMATION = (
        28,
        "thumb-19",
        "styles_v4",
        ", clay animation, as a claymation character, claymation style, animation key shot, plasticine, clay animation, stopmotion animation, aardman character design, plasticine models",
    )
    EUPHORIC = (
        28,
        "thumb-20",
        "styles_v4",
        ", digital illustration, style of charlie bowater, dreamy colorful cyberpunk colors, euphoric fantasy, epic dreamlike fantasy landscape, beautiful oil matte painting, 8k fantasy art, fantasy art landscape, jessica rossier color scheme, dreamlike diffusion",
    )
    MEDIEVAL = (
        28,
        "thumb-21",
        "styles_v4",
        ", movie still from game of thrones, powerful fantasy epic, middle ages, lush green landscape, olden times, roman empire, 1400 ce, highly detailed background, cinematic lighting, 8k render, high quality, bright colours",
    )
    ORIGAMI = (
        28,
        "thumb-22",
        "styles_v4",
        ", polygonal art, layered paper art, paper origami, wonderful compositions, folded geometry, paper craft, made from paper",
    )
    POP_ART = (
        28,
        "thumb-23",
        "styles_v4",
        ", pop art painting, detailed patterns pop art, silkscreen pop art, pop art poster, roy lichtenstein style",
    )
    RENAISSANCE = (
        28,
        "thumb-24",
        "styles_v4",
        ", renaissance period, neo-classical painting, italian renaissance workshop, pittura metafisica, raphael high renaissance, ancient roman painting, michelangelo painting, Leonardo da Vinci, italian renaissance architecture",
    )
    FANTASY = (
        28,
        "thumb-25",
        "styles_v4",
        ", fantasy matte painting,  fantasy landscape, ( ( thomas kinkade ) ), whimsical, dreamy, alice in wonderland, daydreaming, epic scene, high exposure, highly detailed, tim white, michael whelan",
    )
    EXTRA_TERRESTRIAL = (
        28,
        "thumb-26",
        "styles_v4",
        ", deepdream cosmic, painting by android jones, cosmic entity, humanoid creature, james jean soft light 4 k, sci fi, extra terrestrial, cinematic",
    )
    WOOLITIZE = (
        28,
        "thumb-27",
        "styles_v4",
        ", cute! c4d, made out of wool, volumetric wool felting, wool felting art, houdini sidefx, rendered in arnold, soft smooth lighting, soft pastel colors",
    )
    NEO_FAUVISM = (
        28,
        "thumb-28",
        "styles_v4",
        ", neo-fauvism painting, neo-fauvism movement, digital illustration, poster art, cgsociety saturated colors, fauvist",
    )
    AMAZONIAN = (
        28,
        "thumb-29",
        "styles_v4",
        ", amazonian cave, landscape, jungle, waterfall, moss-covered ancient ruins, Dramatic lighting and intense colors, mesmerizing details of the environment and breathtaking atmosphere",
    )
    SHAMROCK_FANTASY = (
        28,
        "thumb-30",
        "styles_v4",
        ", shamrock fantasy, fantasy, vivid colors, grapevine, celtic fantasy art, lucky clovers, dreamlike atmosphere, captivating details, soft light and vivid colors",
    )
    ABSTRACT_VIBRANT = (
        28,
        "thumb-31",
        "styles_v4",
        ", vibrant, editorial, abstract elements, colorful, color splatter, realism, Inspired by the style of Ryan Hewett, dynamic realism, soft lighting and intricate details",
    )
    NEON = (
        28,
        "thumb-32",
        "styles_v4",
        ", neon art style, night time dark with neon colors, blue neon lighting, violet and aqua neon lights, blacklight neon colors, rococo cyber neon lighting",
    )
    CUBISM = (
        28,
        "thumb-33",
        "styles_v4",
        ", cubist picasso, cubism,  a cubist painting, heavy cubism, cubist painting, by Carlo Carrà, style of picasso, modern cubism, futuristic cubism",
    )
    BAUHAUS = (
        28,
        "thumb-34",
        "styles_v4",
        ", Bauhaus art movement,  by Wassily Kandinsky, bauhaus style painting, geometric abstraction, vibrant colors, painting",
    )
    ROCOCCO = (
        28,
        "thumb-35",
        "styles_v4",
        ", francois boucher oil painting, rococco style,  rococco lifestyle, a flemish Baroque, by Karel Dujardin, vintage look, cinematic hazy lighting",
    )
    HAUNTED = (
        28,
        "thumb-36",
        "styles_v4",
        ", horror cgi 4 k, scary color art in 4 k, horror movie cinematography, insidious, la llorona, still from animated horror movie, film still from horror movie, haunted, eerie, unsettling, creepy",
    )
    LOGO = (
        28,
        "thumb-37",
        "styles_v4",
        ", creative logo, unique logo, visual identity, geometric type, graphic design, logotype design, brand identity, vector based, trendy typography, best of behance",
    )
    WATERBENDER = (
        28,
        "thumb-38",
        "styles_v4",
        ", water elements, fantasy, water, exotic, A majestic composition with water elements, waterfall, lush moss and exotic flowers, highly detailed and realistic, dynamic lighting",
    )
    FIREBENDER = (
        28,
        "thumb-39",
        "styles_v4",
        ", fire elements, fantasy, fire, lava, striking. A majestic composition with fire elements, fire and ashes surrounding, highly detailed and realistic, cinematic lighting",
    )
    KAWAII_CHIBI = (
        28,
        "thumb-40",
        "styles_v4",
        ", kawaii chibi romance, fantasy, illustration, Colorful idyllic cheerful, Kawaii Chibi inspired",
    )
    FORESTPUNK = (
        28,
        "thumb-41",
        "styles_v4",
        ", forestpunk, vibrant, HDRI, organic motifs and pollen in the air, bold vibrant colors and textures, spectacular sparkling rays, photorealistic quality with Hasselblad",
    )
    ELVEN = (
        28,
        "thumb-42",
        "styles_v4",
        ", elven lifestyle, photoreal, realistic, 32k quality, crafted by Elves and engraved in copper, elven fantasy land, hyper detailed",
    )
    SAMURAI = (
        28,
        "thumb-43",
        "styles_v4",
        ", samurai lifesyle, miyamoto musashi, Japanese art, ancient japanese samurai, feudal japan art, feudal japan art",
    )
    AQUASTIC = (
        28,
        "thumb-44",
        "styles_v4",
        ", graceful movement with intricate details, inspired by artists like Lotte Reiniger, Carne Griffiths and Alphonse Mucha. Dreamy and surreal atmosphere, twirling in an aquatic landscape with water surface",
    )
    VIBRAN_VIKING = (
        28,
        "thumb-45",
        "styles_v4",
        ", Viking era, digital painting, pop of colour, forest, paint splatter, flowing colors, Background of lush forest and earthy tones, Artistic representation of movement and atmosphere",
    )
    ABSTRACT_CITYSCAPE = (
        28,
        "thumb-46",
        "styles_v4",
        ", abstract cityscape, Ultra Realistic Cinematic Light abstract, futuristic, cityscape, Out of focus background and incredible 16k resolution produced in Unreal Engine 5 and Octan render",
    )
    ILLUSTRATION = (
        28,
        "thumb_31",
        "styles_v1",
        ", minimalistic vector art, illustrative style, style of ian hubert, style of gilles beloeil, inspired by Hsiao-Ron Cheng, style of jonathan solter, style of alexandre chaudret, by Echo Chernik",
    )
    PAINTING = (
        28,
        "thumb_32",
        "styles_v1",
        ", atmospheric dreamscape painting, by Mac Conner, vibrant gouache painting scenery, vibrant painting, vivid painting, a beautiful painting, dream scenery art, instagram art, psychedelic painting, lofi art, bright art",
    )
    ICON = (
        28,
        "thumb_43",
        "styles_v1",
        ", single vector graphics icon, ios icon, smooth shape, vector",
    )
    RENDER = (
        28,
        "thumb_36",
        "styles_v1",
        ", isometric, polaroid octane render, 3 d render 1 5 0 mm lens, keyshot product render, rendered, keyshot product render pinterest, 3 d product render, 3 d cgi render, 3d cgi render, ultra wide angle isometric view",
    )
    COLORING_BOOK = (
        28,
        "thumb-67",
        "styles_v4",
        ", line art illustration, lineart behance hd, illustration line art style, line art colouring page, decora inspired illustrations, coloring pages, digital line-art, line art!!, thick line art, coloring book page, clean coloring book page, black ink line art, coloring page, detailed line art",
    )
    PAPERCUT_STYLE = (
        28,
        "thumb_39",
        "styles_v1",
        ", layered paper art, paper modeling art, paper craft, paper art, papercraft, paper cutout, paper cut out collage artwork, paper cut art",
    )
    KNOLLING_CASE = (
        28,
        "thumb_45",
        "styles_v1",
        ", in  square glass case,  glass cube, glowing, knolling case, ash thorp, studio background,  desktopography, cgsociety 9,  cgsociety, mind-bending digital art",
    )
    PIXEL_ART = (
        28,
        "thumb_38",
        "styles_v1",
        ", one pixel brush, pixelart, colorful pixel art",
    )
    INTERIOR = (
        28,
        "thumb_40",
        "styles_v1",
        ", modern architecture by makoto shinkai, ilya kuvshinov, lois van baarle, rossdraws and frank lloyd wright",
    )
    STICKER = (
        28,
        "thumb_35",
        "styles_v1",
        ", sticker, sticker art, symmetrical sticker design, sticker - art, sticker illustration, die - cut sticker",
    )
    CYBERPUNK = (
        28,
        "thumb_41",
        "styles_v1",
        ",  synthwave image, (neotokyo), dreamy colorful cyberpunk colors, cyberpunk blade runner art, retrofuturism, cyberpunk, beautiful cyberpunk style, cgsociety 9",
    )
    LANDSCAPE = (
        28,
        "thumb_44",
        "styles_v1",
        ", landscape 4k, beautiful landscapes, nature wallpaper, 8k photography",
    )
    ARCHITECTURE = (
        28,
        "thumb_47",
        "styles_v1",
        ", modern architecture design, luxury architecture, bright, very beautiful, trending on unsplash, breath taking",
    )
    GLASS_ART = (
        28,
        "thumb_46",
        "styles_v1",
        ", inside glass ball, translucent sphere, cgsociety 9, glass orb, behance, polished, beautiful digital artwork, exquisite digital art, in a short round glass vase, octane render",
    )
    SCATTER = (
        28,
        "thumb_42",
        "styles_v1",
        ", breaking pieces, exploding pieces, shattering pieces,  disintegration, contemporary digital art, inspired by Dan Hillier, inspired by Igor Morski, dramatic digital art, behance art, cgsociety 9, 3d advanced digital art, mind-bending digital art, disintegrating",
    )
    RETRO = (
        28,
        "thumb_30",
        "styles_v1",
        ", retro futuristic illustration, featured on illustrationx, art deco illustration, beautiful retro art, stylized digital illustration, highly detailed vector art, ( ( mads berg ) ), automotive design art, epic smooth illustration, by mads berg, stylized illustration, ash thorp khyzyl saleem, clean vector art",
    )
    POSTER_ART = (
        27,
        "thumb-56",
        "styles_v4",
        ", album art, Poster, layout, typography, logo, risography, ghibili, simon stalenhag, insane detail, artstation, 8k",
    )
    INK = (
        27,
        "thumb-50",
        "styles_v4",
        ", Black Ink, Hand drawn, Minimal art, artstation, artgem, monochrome",
    )
    JAPANESE_ART = (27, "thumb-51", "styles_v4", ", Ukiyoe, illustration, muted colors")
    SALVADOR_DALI = (
        27,
        "thumb-58",
        "styles_v4",
        ", Painting, by salvador dali, allegory, surrealism, religious art, genre painting, portrait, painter, still life",
    )
    VAN_GOGH = (27, "thumb-61", "styles_v4", ", painting, by van gogh")
    STEAMPUNK = (
        27,
        "thumb-60",
        "styles_v4",
        ", steampunk, stylized digital illustration, sharp focus, elegant, intricate, digital painting, artstation concept art, global illumination, ray tracing, advanced technology, chaykan howard, campion pascal, cooke darwin, davis jack, pink atmosphere",
    )
    RETROWAVE = (
        27,
        "thumb-57",
        "styles_v4",
        ", Illustration, retrowave art, noen light, retro, digital art, trending on artstation",
    )
    POLY_ART = (
        27,
        "thumb-55",
        "styles_v4",
        ", low poly, artstation, studio lightning, stainless steel, grey color scheme",
    )
    VIBRANT = (
        27,
        "thumb-62",
        "styles_v4",
        ", Psychedelic, water colors spots, vibrant color scheme, highly detailed, romanticism style, cinematic, artstation, greg rutkowski",
    )
    MYSTICAL = (
        27,
        "thumb-52",
        "styles_v4",
        ", fireflies, deep focus, d&d, fantasy, intricate, elegant, highly detailed, digital painting, artstation, concept art, matte, sharp focus, illustration, hearthstrom, gereg rutkowski, alphonse mucha, andreas rocha",
    )
    CINEMATIC_RENDER = (
        27,
        "thumb-47",
        "styles_v4",
        ", cinematic, breathtaking colors, close-up, cgscociety, computer rendering, by mike winkelmann, uhd, rendered in cinema4d, surface modeling, 8k, render octane, inspired by beksinski",
    )
    FUTURISTIC = (
        27,
        "thumb-49",
        "styles_v4",
        ", futuristic, elegant atmosphere, glowing lights, highly detailed, digital painting, artstation, concept art, smooth sharp focus, illustration, mars ravelo, gereg rutkowski",
    )
    POLAROID = (27, "thumb-54", "styles_v4", ", old polaroid, 35mm")
    PICASO = (27, "thumb-53", "styles_v4", ", painting, by pablo picaso, cubism")
    SKETCH = (27, "thumb-59", "styles_v4", ", pencil, hand drawn, sketch, on paper")
    COMIC_BOOK = (
        28,
        "thumb-48",
        "styles_v4",
        ", Comic cover, 1960s marvel comic, comic book illustrations",
    )


class Ratio(Enum):
    """Enum for the different image ratios."""

    RATIO_1X1 = (512, 512)
    RATIO_9X16 = (368, 648)
    RATIO_16X9 = (648, 368)
    RATIO_4X3 = (512, 384)
    RATIO_3X2 = (648, 432)


class Control(Enum):
    """Enum for the different controls."""

    SCRIBBLE = "scribble"
    POSE = "openpose"
    DEPTH = "depth"


class DeviantArt(Enum):
    """Enum for the DeviantArt API credentials."""

    ID = 23185
    SECRET = "fae0145a0736611056a5196a122c0d36"


def validate_cfg(cfg: float) -> str:
    """Validates the cfg parameter."""
    if cfg < 0.0 or cfg > 16.0:
        raise ValueError(f"Invalid CFG, must be in range (0; 16), {cfg}")
    return str(cfg)


class AsyncImagine:
    """Async class for handling API requests to the Imagine service."""

    HEADERS = {"accept": "*/*", "user-agent": "okhttp/4.10.0"}

    def __init__(self):
        self.asset = "https://1966211409.rsc.cdn77.org"
        self.api = "https://inferenceengine.vyro.ai"
        self.session = aiohttp.ClientSession(
            raise_for_status=True, headers=self.HEADERS
        )
        self.version = "1"

    async def close(self) -> None:
        """Close async session"""
        return await self.session.close()

    def get_style_url(self, style: Style = Style.IMAGINE_V1) -> str:
        """Get link of style thumbnail"""
        return f"{self.asset}/appStuff/imagine-fncisndcubnsduigfuds//assets/{style.value[2]}/{style.value[1]}.webp"

    def bytes_to_io(self, data: bytes, filename: str) -> io.BytesIO:
        """Convert bytes to io.BytesIO with name for sending"""
        bio = io.BytesIO(data)
        bio.name = filename
        return bio

    async def assets(self, style: Style = Style.IMAGINE_V1) -> bytes:
        """Gets the assets."""
        async with self.session.get(url=self.get_style_url(style=style)) as resp:
            return await resp.read()

    async def variate(
        self, image: bytes, prompt: str, style: Style = Style.IMAGINE_V1
    ) -> bytes:
        async with self.session.post(
            url=f"{self.api}/variate",
            data={
                "model_version": self.version,
                "prompt": prompt + (style.value[3] or ""),
                "strength": "0",
                "style_id": str(style.value[0]),
                "image": self.bytes_to_io(image, "image.png"),
            },
        ) as resp:
            return await resp.read()

    async def sdprem(
        self,
        prompt: str,
        negative: str = None,
        priority: str = None,
        steps: str = None,
        high_res_results: str = None,
        style: Style = Style.IMAGINE_V1,
        seed: str = None,
        ratio: Ratio = Ratio.RATIO_1X1,
        cfg: float = 9.5,
    ) -> bytes:
        """Generates AI Art."""
        try:
            validated_cfg = validate_cfg(cfg)
        except Exception as e:
            print(f"An error occurred while validating cfg: {e}")
            return None

        try:
            async with self.session.post(
                url=f"{self.api}/sdprem",
                data={
                    "model_version": self.version,
                    "prompt": prompt + (style.value[3] or ""),
                    "negative_prompt": negative or "",
                    "style_id": style.value[0],
                    "width": ratio.value[0],
                    "height": ratio.value[1],
                    "seed": seed or "",
                    "steps": steps or "30",
                    "cfg": validated_cfg,
                    "priority": priority or "0",
                    "high_res_results": high_res_results or "0",
                },
            ) as resp:
                return await resp.read()
        except Exception as e:
            print(f"An error occurred while making the request: {e}")
            return None

    async def upscale(self, image: bytes) -> bytes:
        """Upscales the image."""
        try:
            async with self.session.post(
                url=f"{self.api}/upscale",
                data={
                    "model_version": self.version,
                    "image": self.bytes_to_io(image, "test.png"),
                },
            ) as resp:
                return await resp.read()
        except Exception as e:
            print(f"An error occurred while making the request: {e}")
            return None

    async def translate(self, prompt: str) -> str:
        """Translates the prompt."""
        async with self.session.post(
            url=f"{self.api}/translate",
            data={"q": prompt, "source": detect(prompt), "target": "en"},
        ) as resp:
            return (await resp.json())["translatedText"]

    async def interrogator(self, image: bytes) -> str:
        """Generates a prompt."""
        async with self.session.post(
            url=f"{self.api}/interrogator",
            data={
                "model_version": str(self.version),
                "image": self.bytes_to_io(image, "prompt_generator_temp.png"),
            },
        ) as resp:
            return await resp.text()

    async def sdimg(
        self,
        image: bytes,
        prompt: str,
        negative: str = None,
        seed: str = None,
        cfg: float = 9.5,
    ) -> bytes:
        """Performs inpainting."""
        async with self.session.post(
            url=f"{self.api}/sdimg",
            data={
                "model_version": self.version,
                "prompt": prompt,
                "negative_prompt": negative or "",
                "seed": seed or "",
                "cfg": validate_cfg(cfg),
                "image": self.bytes_to_io(image, "image.png"),
            },
        ) as resp:
            return await resp.read()

    async def controlnet(
        self,
        image: bytes,
        prompt: str,
        negative: str = None,
        cfg: float = 9.5,
        control: Control = Control.SCRIBBLE,
        style: Style = Style.IMAGINE_V1,
        seed: str = None,
    ) -> bytes:
        """Performs image remix."""
        async with self.session.post(
            url=f"{self.api}/controlnet",
            data={
                "model_version": self.version,
                "prompt": prompt + (style.value[3] or ""),
                "negative_prompt": negative or "",
                "strength": "0",
                "cfg": validate_cfg(cfg),
                "control": control.value,
                "style_id": str(style.value[0]),
                "seed": seed or "",
                "image": self.bytes_to_io(image, "image.png"),
            },
        ) as resp:
            return await resp.read()


def run():
    if not USERNAME or not SERVER or not PASSWORD:
        print(
            "Please set the environment variables MATRIX_USERNAME(optional), MATRIX_SERVER(optional), and MATRIX_PASSWORD(required)"
        )
        return

    creds = botlib.Creds(SERVER, USERNAME, PASSWORD)
    bot = botlib.Bot(creds)

    @bot.listener.on_message_event
    async def ask(room, message):
        match = botlib.MessageMatch(room, message, bot, PREFIX)

        if match.is_not_from_this_bot() and match.prefix() and ENABLE_AI_COMMAND:
            for alias in AI_COMMAND_ALIASES:
                if match.command(alias):
                    break
            else:
                return

            try:
                prompt = " ".join(arg for arg in match.args())
                response = "".join(Completion.create(prompt))
                await bot.api.send_markdown_message(
                    room.room_id, f"> {prompt}\n\n{response}"
                )
            except Exception as e:
                print(e)
                await bot.api.send_markdown_message(room.room_id, f"> {prompt}\n\n{e}")
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(PING_URL) as resp:
                        await resp.read()

    @bot.listener.on_message_event
    async def image(room, message):
        match = botlib.MessageMatch(room, message, bot, PREFIX)

        if match.is_not_from_this_bot() and match.prefix() and ENABLE_IMAGE_COMMAND:
            for alias in IMAGE_COMMAND_ALIASES:
                if match.command(alias):
                    break
            else:
                return

            try:
                print(match.args())
                prompt = ""
                negative = ""

                style = "IMAGINE_V3"
                ratio = "RATIO_1X1"

                for arg in match.args():
                    if arg.startswith("neg="):
                        negative += arg.replace("neg=", "")

                    elif arg.startswith("style="):
                        style = arg.replace("style=", "")

                    elif arg.startswith("ratio="):
                        ratio = arg.replace("ratio=", "")
                    else:
                        prompt += arg + " "

                async def generate_image(
                    image_prompt, style_value, ratio_value, negative
                ):
                    imagine = AsyncImagine()
                    filename = str(uuid.uuid4()) + ".png"
                    try:
                        style_enum = Style[style_value]
                        ratio_enum = Ratio[ratio_value]
                    except KeyError:
                        style_enum = Style.IMAGINE_V3
                        ratio_enum = Ratio.RATIO_1X1
                    img_data = await imagine.sdprem(
                        prompt=image_prompt,
                        style=style_enum,
                        ratio=ratio_enum,
                        priority="1",
                        high_res_results="1",
                        steps="70",
                        negative=negative,
                    )

                    try:
                        with open(filename, mode="wb") as img_file:
                            img_file.write(img_data)
                    except Exception as e:
                        print(f"An error occurred while writing the image to file: {e}")
                        return None

                    await imagine.close()

                    return filename

                filename = await generate_image(prompt, style, ratio, negative)

                await bot.api.send_image_message(
                    room_id=room.room_id, image_filepath=filename
                )

            except Exception as e:
                print(e)
                await bot.api.send_markdown_message(room.room_id, f"> {prompt}\n\n{e}")

            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(PING_URL) as resp:
                        await resp.read()

    @bot.listener.on_message_event
    async def bot_help(room, message):
        styles = ", ".join([style.name for style in Style])
        ratios = ", ".join([ratio.name for ratio in Ratio])
        bot_help_message = f"""
Help Message:
    prefix: {PREFIX}
    commands:
        help:
            command: help, ?, h
            description: display help command
        ask:
            command: {", ".join(AI_COMMAND_ALIASES)}
            description: ask gpt a question
        img:
            command: {", ".join(IMAGE_COMMAND_ALIASES)}
            description: generate an image from a prompt
            options:
                neg:
                    description: negative prompt
                    example: neg=low
                style:
                    description: style of image
                    example: style=IMAGINE_V3
                    values: {styles}
                ratio:
                    description: ratio of image
                    example: ratio=RATIO_1X1
                    values: {ratios}

            """
        match = botlib.MessageMatch(room, message, bot, PREFIX)
        if (
            match.is_not_from_this_bot()
            and match.prefix()
            and (match.command("help") or match.command("?") or match.command("h"))
        ):
            await bot.api.send_text_message(room.room_id, bot_help_message)

    try:
        bot.run()
    except Exception as e:
        subprocess.run(["systemctl", "restart", "--user", SYSTEMD_SERVICE_NAME])
        print("Restarting bot due to {e}")
        return 1


if __name__ == "__main__":
    sys.exit(run())
