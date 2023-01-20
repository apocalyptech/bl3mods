Mega TimeSaver XL
=================

This mod aims to speed up nearly all the noticeably-slow interactive
objects that you use throughout BL3.  It's focused mostly on things you
directly interact with, though it does include other speedups like NPC
walking speeds, where appropriate.  The mod doesn't attempt to do any
dialogue or mission skips -- all content in the game should still be
available.

**NOTE:** Parts of this mod currently *require* using
[OpenHotfixLoader (OHL)](https://borderlandsmodding.com/bl3-running-mods/#ohl-openhotfixloader)
instead of B3HM.  If B3HM v1.0.2 ever gets released, that version
should be supported too, but v1.0.1 will *not* give you 100% mod
functionality with this mod.

A sampling of the things this mod affects:

* Lootable Containers, Doors, Elevators, Slot Machines, Lost Loot Machine, etc...
* Vehicle interaction animations (hijacking, entering, leaving, changing seats)
* Catch-A-Ride Digistruct Speed
* Fast Travel / Teleport / Respawning (no more digistruct tunnel!)
* Eridian tools (Resonator, Analyzer)
* Removed startup countdown for: Takedown at the Maliwan Blacksite,
  Takedown at the Guardian Breach, and Arm's Race
* A *lot* of mission-and-map-specific animations throughout the game
* Many characters' walking/sprinting speeds have been improved.  The speedup
  is, in general, a little less than
  [CZ47's Faster NPCs mod](https://github.com/BLCM/bl3mods/wiki/Faster%20NPCs),
  so execute that one after this one if you want some NPCs to be even faster.
  The list of affected NPCs is a bit different between the two, as well.
  Characters affected by this mod:
  * Ace Baron (from Healers and Dealers)
  * Ava (base game and DLC6 version)
  * Brick
  * BUD Bot
  * Bureaucracy Bot (Form Bot)
  * Clay (base game and DLC6 version)
  * Claptrap (base game and DLC6 version)
  * Digby Vermouth
  * Drunk William (from Quick and the Quickerer)
  * Ellie
  * Failurebot
  * Gaige
  * Glenn the Ratch
  * Joy
  * Liam (Atlas HQ Guard)
  * Lilith
  * Maya
  * McSmugger
  * Oletta
  * P.A.T.
  * Slim (from Quick and the Quickerer)
  * Terry the Ratch
  * Timothy Lawrence
  * Tina
  * Typhon
  * Vic (from Head Case)
  * VIP Valet

Known Quirks
============

These aren't really bugs per se, just side-effects of having all these
speedups in effect.  See the Known Bugs section below, as well!

* The increased opening speed on some containers which fling loot
  into the air seems to cause the loot to sometimes fly away at
  pretty high speeds.  This can be a bit annoying in cases like the
  trash collection in Spendopticon during One Man's Treasure.
* To get on top of the "main" elevator in Meridian Outskirts (to reach the
  Typhon Dead Drop), you'll likely either have to use Photo Mode to hit
  the elevator button, or go the long way around after moving the elevator
  to the bottom.
* It's very easy to end up with skipped dialogue at the top of the Tazendeer
  Elevator -- there's some triggers up there which can be missed if there's
  already dialogue playing.  This mod moves one of those around a bit so it no
  longer triggers right at the top of the now-sped-up elevator, so if you want
  to make sure to hear all the Typhon+Tyreen dialogue up there, make sure to
  wait around for dialogue lines to finish before pressing onward.
* During Jack's Wild, the elevator in Jack's Secret stops further down than
  usual, and well before Pretty Boy's usual cue, but there's still a window
  right there and you can jump out as usual once he's done talking.
* In Obsidian Forest, when Oletta's on her way to the Traitorweed testing
  area, if you stay too close to her she may end up teleporting to her next
  nav point (and skipping some dialogue in the process).  Hang back a bit to
  avoid that!

Not Handled By This Mod
=======================

Some things intentionally *not* handled by the mod, either because they were
already pretty good speedwise, because speedups would've caused dialogue
skips, or because it just felt right to leave 'em alone:

* Inter-system navigation via Sanctuary III
* Using the Viper Drive in Skywell-27, during Space-Laser Tag.  Those delays
  are all pretty dialogue-dependent.
* Chadd's movement in Floodmoor Basin, during Swamp Bro.  Most of the slow
  bits are shared animations like climbing ledges and so on.
* The Boosty-Jammer elevator in Floodmoor Basin
* The bomb conveyor in Floodmoor Basin, during Capture the Frag.  Speeding
  that one up can cause clipping through other conveyors, in addition to
  dialogue skips.
* The crane in Ambermire.  That sequence is mostly dialogue-dependent.
* The Rakk shootout in Devil's Razor, during Life of the Party.  Use my
  [Life of the Party: Short Rakk Shootout](https://github.com/BLCM/bl3mods/wiki/Life%20of%20the%20Party%3A%20Short%20Rakk%20Shootout)
  mod to shorten that, if you want.
* The Desolation's Edge mission "Homeopathological"
* The explosive device delay in Desolation's Edge, during Bad Vibrations
* The Desolation's Edge mission "Transaction-Packed."  I recommend using my
  [Transaction-Packed: Abridged](https://github.com/BLCM/bl3mods/wiki/Transaction-Packed%3A%20Abridged)
  mod to basically skip the entire mission, instead.
* The cube animations during Mysteriouslier: Horror at Scryer's Crypt
* The sequence of meeting Timothy for the first time in Spendopticon could
  probably be improved in various ways, but it got complex enough that I
  didn't bother, in the end.
* Likewise, various aspects of the Digby Vermouth quests in Spendopticon
  could use a kick, but apart from improving his walk/run speed, they were
  left alone.
* The picnic section in The Compactor, during Heart of Gold.  It's not bad
  in the first place.
* The Clapstructor sequence could be tightened up slightly, but not by much.
* The whole Raging Bot mission (in Spendopticon) could be tightened up in
  various ways, but seemed too annoying to wade through for pretty small gains.
* The drawbridge lowering in The Cankerwood
* Various sequences during Cold Case: Forgotten Answers, in The Cankerwood
* Daisy's door-opening in Blastplains has been left alone; it's nice and
  dramatic.
* Adding the various bath products during Dirty Deeds, in Ashfall Peaks
* Telezapper registration in The Blastplains
* The cocking animation on the third catapult in Castle Crimson has been
  left alone, for boring technical reasons.
* The egg-incubation timer in Castle Crimson, during A Good Egg
* The whole train-rotation and subsequent mallet-propulsion in Sapphire's
  Run has been left alone.  The rotation is already pretty quick, and I
  think speeding up the mallet-hit would take away from the humor of the
  situation.
* Statue Krieg opening the gate to Vaulthalla

Known Bugs / TODO
=================

* Vehicle-related animations are a bit weird in general.  The animations tend
  to get "frozen" near the end for a bit.  Also, weapons on vehicles that you
  hijack seem to take a little while to become active, possibly based on timing
  from the original hijack animations?  Also hijacked-vehicle steering might
  be similarly locked out for a bit (though acceleration is still possible).
  Anyway, it's strange, and unfortuantely I currently have zero ideas on how
  to address it (beyond simply *not* speeding up vehicle animations, of course).
* Respawning after death leaves your char facing the wrong way.
* Pickups flung into the air don't auto-pick-up until they're no longer
  affected by physics (like loot from bone piles, trash cans, etc).
* Iron Bear interactions (entering, exiting, Dakka Bear turret)?  I'm leaving
  those alone primarily out of laziness but also because that'd feel like an
  actual combat advantage, which isn't really something this mod is meant to
  do (though I suppose our vehicle handling technically applies to that).
* The Vault Card Chest-opening tweak does *not* work in Pyre of Stars.
* The door you have to slide under to retrieve the umbrella for
  Claptrap in Bad Reception acts a bit weirdly, and is probably
  pretty easy to just run through now.
* The locker holding Ember's tools, in Freddie's lair in Impound
  Deluxe, doesn't open all the way when BUD Bot opens it up for you.
  The tools are still easily-grabbable, though.
* Oletta ends up teleporting a bit during the Obsidian Forest side mission
  Lost and Found, when she first jumps down onto the rooftops.
* Speed of camera that moves in/out of Photo Mode?
* Ammo containers seem to not always attach ammo properly; ends up below the
  platform (at least, the sort 'round Tannis's dig site in The Droughts, and
  in Athenas).  Seems to be maybe not consistent, though?  Sometimes it seems
  to work.  Possibly relatedly, sometimes Eridian ammo chests seem to not open
  all the way.  I think all the ammo inside remains pick-uppable, though, and
  I can't reliably reproduce the behavior.
* Diamond Armory console?
* I ended up reducing `global_scale` from 5 to 4 at the end of Athenas, because
  the other container tightening I did there ended up making them sort of seem
  *too* fast.  Even at 4x, things still seem quite good, IMO.  May want to
  doublecheck some stuff from before then, though, to just to be sure:
  * Statue printer/scanner
  * Taking Flight elevator
  * Meridian Outskirts elevators
* Unrelatedly to re-test:
  * Moxxi slot-machine eridium bump
  * Re-test `City_P` hub door-opening (tweaked that during `OrbitalPlatform_P`)
  * Also the Skywell-27 door after the thruster disabling
  * Maybe *everything* up through Athenas?  When I got to Pyre of Stars, I discovered
    that our Vault Card Chest speedup causes some mission event to Not Work Anymore
    (specifically at the very beginning when Tannis and Typhon run up to the door,
    and it opens -- the door will open but Tannis and Typhon will remain stuck there).
    The Vault Card Chest addition happened after I was through on Athenas.
* Did we want to do the "initial" ECHO playing animation, with the blowing-on-cart?
* Blackjack tables in DLC1 seem to not actually show all your cards; if we're not
  already doing sequencelength->1 stuff, perhaps that'll do it.

Changelog
=========

**v1.0.0** - *(unreleased)*
 * Reduced our "standard" speed improvement from 5x to 4x (except for doors)
 * Fixed Typhon Dead Drop Chests
 * Tightened up various chest-opening animations (including digistruct contents)
 * Character Movement Speed:
   * Ace Baron (from Healers and Dealers)
   * Ava (base game and DLC6 version)
   * Brick
   * BUD Bot
   * Bureaucracy Bot (Form Bot)
   * Claptrap (DLC6 version)
   * Clay (base game and DLC6 version)
   * Digby Vermouth
   * Drunk William (from Quick and the Quickerer)
   * Ellie
   * Failurebot
   * Gaige
   * Glenn the Ratch
   * Joy
   * Liam (Atlas HQ guard)
   * Maya
   * McSmugger
   * Oletta
   * P.A.T.
   * Slim (from Quick and the Quickerer)
   * Terry the Ratch
   * Timothy Lawrence
   * Tina
   * Typhon
   * Vic (from Head Case)
   * VIP Valet
 * Elevators!
 * Extra Doors:
   * Meridian Metroplex hub door
   * Skywell-27 post-thruster-disabling door
   * Gate to the back half of the Homestead, in Splinterlands
   * Largeish Eridian doors in Pyre of Stars
   * Entrance to Timothy's hideout in The Spendopticon
   * Crypt-opening door in Cold Case: Buried Questions, in Cursehaven
   * A couple doors from DLC6
 * Other Additions:
   * Slot Machines
   * Lost Loot Machine
   * Vault Card chest-opening animation (except in Pyre of Stars)
   * Fast-travel/teleport/resurrect skips
   * ECHO cartridge playing animation
 * Mission-Specific Animations:
   * Statue scanner/printer from Golden Calves
   * Coffee-pouring animation during Rise and Grind (pretty slight improvement,
     and if localization dialogue other than English happens to be longer, it's
     possible that some dialogue might get cut off)
   * Second Bell-of-Peace door opening on Athenas
   * Rhys's sliding desk in Atlas HQ
   * Ava's shock reaction after Maya's death
   * Pippie digging animation in Witch's Brew
   * Lots of Jakobs Estate-specific animations: exploding statues, sliding
     portraits, spinning bookshelves, stage props
   * Sliding bed in "Sacked"
   * Chasm-jump timer in Rumble in the Jungle
   * BALEX / EMS Bot door-opening scanning
   * Splinterlands Car Grinder
   * Golden Chariot crane-lowering
   * Fragile overhead pipe in Konrad's Hold
   * Handsome Jack portrait in Konrad's Hold
   * Eridian statue rotation in Tazendeer Ruins
   * Some tweaks to a dialogue trigger at the top of the Tazendeer Ruins
     elevator
   * Bridge-raising animation at the top of Tazendeer Ruins elevator
   * Rising Eridian statues in Pyre of Stars
   * Rising platforms in Pyre of Stars
   * Rocket launch in Fire in the Sky
   * Removed start countdown in Arm's Race
   * Initial crystal pads in Guardian Takedown, on Minos Prime
   * Bookshelf puzzle in Villa Ultraviolet
   * Descending fountain in Villa Ultraviolet
   * Hyperway travel in The Spendopticon
   * Bridge extension back to Freddie's lair at the end of Impound Deluxe
   * "Key To Happiness" timer in The Compactor, on the way into Trashlantis
   * Ultra-Thermite opening the door to VIP Tower
   * Various Call of the Deep tweaks, in Skittermaw basin: power coil panel, crane
     animations, Gythian blood jar.
   * Mission-close delay after returning recordings to DJ Midnight in The Lodge
   * Secret wall in crypt in Cursehaven
   * Brew-mixing machinery in The Cankerwood
   * Desk drawers in hidden elevator in Heart's Desire
   * Artillery cannon for Money Back Guarantee, in The Blastplains
   * Castle Crimson catapult animations
   * Don't Call it A Rorschach Ink-Blot Pipes, in Benediction of Pain

Aug 1, 2022 *(no version number change)*
 * Updated to use [new metadata tags](https://github.com/apple1417/blcmm-parsing/tree/master/blimp)
   (no functionality change)

Jun 16, 2021 *(no version number change)*
 * Added contact info to mod header

**v0.9.1** - May 10, 2021
 * Mod file was rebuilt using some updated backend infrastructure; no
   actual changes, but some values changed from integers to floats
   (`1000` -> `1000.0`, for instance)

**v0.9.0** - March 10, 2021
 * Initial beta release.  Incomplete, but should be handy regardless!
 
Licenses
========

This mod is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The generation script for the mod is licensed under the
[GPLv3 or later](https://www.gnu.org/licenses/quick-guide-gplv3.html).
See [COPYING.txt](../../COPYING.txt) for the full text of the license.

