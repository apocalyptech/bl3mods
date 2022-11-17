Mega TimeSaver XL
=================

This mod aims to speed up nearly all the noticeably-slow interactive
objects that you use throughout BL3.  It will eventually hope to encompass
basically the entire game, but **it is currently a work in progress!**

As such, this mod has not seen an awful lot of testing, so please let me
know if there's anything game-breaking or Obviously Wrong with this (like
if a too-fast animation ends up breaking mission progression somewhere).

Currently, the mod affects the following:

* Lootable Containers
* Doors
* Vehicle interaction animations (hijacking, entering, leaving, changing seats)
* Catch-A-Ride Digistruct Speed
* Various characters' walking/sprinting speeds have been improved.  The speedup
  is, in general, a little less than CZ47's Faster NPCs mod, so execute that
  one after this one if you want some NPCs to be even faster.  The list of
  affected NPCs is a bit different between the two, as well.  Characters
  affected by this mod:
  * Ace Baron (from Healers and Dealers)
  * Ava
  * Claptrap
  * Ellie
  * Glenn the Ratch
  * Liam (Atlas HQ Guard)
  * Lilith
  * Maya
  * Terry the Ratch
  * Vic (from Head Case)
* Eridian tools (Resonator, Analyzer)
* Fast-Travel/Teleport and Respawn animations

Note that the vehicle animations in particular are a bit weird right now --
the animation gets "frozen" near the end for a bit.  I think that's something
that we can't do much about at the moment, though I'll be looking into it
more for the eventual 1.0 release.  Check the full README for known bugs and
my current TODO!

**NOTE:** The Vault Card Chest-opening speed tweak currently *requires*
using OpenHotfixLoader (OHL) instead of B3HM.  If B3HM v1.0.2 ever gets
released, that version should be supported too, but v1.0.1 will *not*
work with that Vault Card chest.

A few known quirks of running with this mod:
* To get on top of the "main" elevator in Meridian Outskirts (to reach the
  Typhon Dead Drop), you'll likely either have to use Photo Mode to hit
  the elevator button, or go the long way around after moving the elevator
  to the bottom.

Some things intentionally *not* handled by the mod:
* The Viper Drive uses in Space-Laser Tag are all pretty dialogue-dependent,
  so I left those alone.
* The Desolation's Edge mission "Transaction-Packed" has been left alone.
  I recommend using my "Transaction-Packed: Abridged" to basically skip
  the entire mission, instead.

Known Bugs
==========

* Weapons on vehicles that you hijack seem to take a little bit to
  become active, possibly based on timing from the original hijack
  animations?  Vehicle movement, at least, is available right away,
  though steering is not.  Hrmph.
* The door you have to slide under to retrieve the umbrella for
  Claptrap in Bad Reception acts a bit weirdly, and is probably
  pretty easy to just run through now.
* Respawning after death leaves your char facing the wrong way.

TODO
====

* It'd be nice to figure out getting the respawn animation to leave the
  camera in the right spot.
* Other character-speed improvements (Oletta comes to mind)
* Pretty much every mission-specific animation
* Elevators
* Lost Loot machine?
* DLC1 Slot Machines
* Delay after breaking bone piles, trash cans, etc (basically pickups which
  aren't actually "connected" to a container)
  * Bone Piles
  * Trash Cans
  * Washing Machines
  * Cardboard Boxes
  * Some Mailbox drops
  * Some porta-potty drops
  * Eridian Crystals
* I feel like the Slam animation could use some work
* Entering/Exiting Iron Bear?
* Maybe have a real slight speedup on melee attacks?
* Speed of camera that moves in/out of Photo Mode?
* Ammo containers seem to not always attach ammo properly; ends up below the
  platform (at least, the sort 'round Tannis's dig site in The Droughts, and
  in Athenas).  Seems to be maybe not consistent, though?  Sometimes it seems
  to work.  Possibly relatedly, sometimes Eridian ammo chests seem to not open
  all the way.  I think all the ammo inside remains pick-uppable, though, and
  I can't reliably reproduce the behavior.
* Diamond Armory console?
* Check CZ47's Faster NPCs mod (and make a note about compatibility, if need be)
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

Changelog
=========

**v1.0.0** - *(unreleased)*
 * Reduced our "standard" speed improvement from 5x to 4x (except for doors)
 * Fixed Typhon Dead Drop Chests
 * Tightened up various chest-opening animations (including digistruct contents)
 * Character Movement Speed:
   * Ace Baron (from Healers and Dealers)
   * Ava
   * Ellie
   * Glenn the Ratch
   * Liam (Atlas HQ guard)
   * Maya
   * Terry the Ratch
   * Vic (from Head Case)
 * Elevators!
 * Extra Doors:
   * Meridian Metroplex hub door
   * Skywell-27 post-thruster-disabling door
   * A couple doors from DLC6
 * Other Additions:
   * Slot Machines
   * Vault Card chest-opening animation
   * Fast-travel/teleport/resurrect skips
 * Mission-Specific Animations:
   * Statue scanner/printer from Golden Calves
   * Coffee-pouring animation during Rise and Grind (pretty slight improvement,
     and if localization dialogue other than English happens to be longer, it's
     possible that some dialogue might get cut off)
   * Second Bell-of-Peace door opening on Athenas
   * Rhys's sliding desk in Atlas HQ

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

