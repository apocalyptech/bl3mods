#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2021-2022 Christopher J. Kucera
# <cj@apocalyptech.com>
# <https://apocalyptech.com/contact.php>
#
# This Borderlands 3 Hotfix Mod is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This Borderlands 3 Hotfix Mod is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this Borderlands 3 Hotfix Mod.  If not, see
# <https://www.gnu.org/licenses/>.

import sys
import argparse
sys.path.append('../../../python_mod_helpers')
from bl3data.bl3data import BL3Data
from bl3hotfixmod.bl3hotfixmod import Mod, BVC, LVL_TO_ENG_LOWER

parser = argparse.ArgumentParser(
        description='Generates Mega TimeSaver XL',
        )
parser.add_argument('-v', '--verbose',
        action='store_true',
        help='Be verbose about what we\'re processing',
        )
args = parser.parse_args()
verbose = args.verbose

mod = Mod('mega_timesaver_xl.bl3hotfix',
        'Mega TimeSaver XL',
        'Apocalyptech',
        [
            "Speeds up animations throughout the game.",
            "",
            "THIS IS A WORK IN PROGRESS!  Please report any game-breaking bugs",
            "to me, but some animations are bound to remain at their original",
            "speed.",
        ],
        contact='https://apocalyptech.com/contact.php',
        lic=Mod.CC_BY_SA_40,
        v='0.9.1',
        cats='qol',
        quiet_streaming=True,
        )

# AnimSequence objects have two attributes of note:
#  1) SequenceLength - total amount of time the sequence is supposed to take.  It
#     looks like just shortening this value works great, but JWP can't currently
#     serialize AnimSequence objects, so we can't automatically pull current values
#     from data.  (FModel *can* serialize them, but we can't automate that like we
#     can with JWP.)
#  2) RateScale - almost certainly this is always just `1`, and this can be set to
#     scale things up easily, to.  So that's what we're going to be using, mostly!

# How much to improve speed
global_scale = 4

# ... but I want to do doors a *bit* more
door_scale = 5

# Character movement speed
global_char_scale = 1.4

# Vehicle-animation movement speed
global_vehicle_scale = 2

# Eridian tool speedups
global_eridian_scale = 2

# Minimum serialization version to allow.  Stock JWP doesn't serialize CurveFloats
# correctly, so the mod'll be invalid unless using apocalyptech's fork, of at least
# this version.
min_apoc_jwp_version = 19

# Data obj
data = BL3Data()

mod.header('Item Pickups')

# Defaults:
#  /Game/GameData/GameplayGlobals
#  - MassPickupMaxDelay: 0.075
#  - MassPickupMaxPullAmount: 6
#  - MassPickupMaxTotalDelay: 1.5
#  - MassPickupMinDelay: 0.06
#  - MassPickupRadius: 400
#  /Game/Pickups/_Shared/_Design/AutoLootContainerPickupFlyToSettings
#  - MaxLifetime: 2.5
#  - SpinSpeed: (pitch=0, yaw=200, roll=200)
#  - LinearSpeed: 750
#  - LinearAcceleration: 650

mod.comment('Mass Pickup Delay (honestly not sure if these have much, if any, effect)')
for var, value in [
        ('MassPickupMaxDelay', 0.075/3),
        ('MassPickupMaxTotalDelay', 1.5/3),
        ('MassPickupMinDelay', 0.06/3),
        ]:
    mod.reg_hotfix(Mod.PATCH, '',
            '/Game/GameData/GameplayGlobals',
            var,
            round(value, 6))
mod.newline()

mod.comment('Pickup flight speeds (likewise, I suspect many of these don\'t actually do much)')
mod.comment('The `AutoLootContainer` ones definitely do help, at least.')
for obj_name in [
        'AutoLootContainerPickupFlyToSettings',
        'ContainerEchoLogPickupFlyToSettings',
        'ContainerPickupFlyToSettings',
        'DroppedEchoLogPickupFlyToSettings',
        'DroppedPickupFlyToSettings',
        ]:
    full_obj_name = f'/Game/Pickups/_Shared/_Design/{obj_name}'
    obj_data = data.get_exports(full_obj_name, 'PickupFlyToData')[0]
    if 'LinearSpeed' in obj_data:
        speed = obj_data['LinearSpeed']
    else:
        # This seems to be the default
        speed = 1000
    mod.reg_hotfix(Mod.PATCH, '',
            full_obj_name,
            'LinearSpeed',
            speed*2)
    mod.reg_hotfix(Mod.PATCH, '',
            full_obj_name,
            'LinearAcceleration',
            obj_data['LinearAcceleration']*2)
mod.newline()

# Vault Card Chest injection!  So: the Vault Card menu uses a custom red chest
# to do the animation, and the chest object in the UI structure also uses a custom
# opening animation.  Those objects don't ordinarily exist until the Vault Card
# menu has been opened, though, and they disappear once the menu is closed.  So,
# our hotfixes can't touch them unless we inject the chest into each map first.
# So that's what we're doing here!  One further wrinkle is that the "stock" custom
# red chest object doesn't actually use the animation that the menu-spawned chest
# uses, so we *also* have to force that reference to exist, so that we can hotfix
# the proper animation.  Just 395 hotfixes (including the actual animation-speedup
# ones) to get this working!  Totally worth it.
mod.header('Vault Card Chest Injection (needed in order to speed up the opening animation)')
for level_full in [
        '/Alisma/Maps/Anger/Anger_P',
        '/Alisma/Maps/Chase/Chase_P',
        '/Alisma/Maps/Eldorado/Eldorado_P',
        '/Alisma/Maps/Experiment/Experiment_P',
        '/Alisma/Maps/Sanctum/Sanctum_P',
        '/Dandelion/Maps/CasinoIntro/CasinoIntro_P',
        '/Dandelion/Maps/Core/Core_P',
        '/Dandelion/Maps/Impound/Impound_P',
        '/Dandelion/Maps/Strip/Strip_P',
        '/Dandelion/Maps/TowerLair/TowerLair_P',
        '/Dandelion/Maps/Trashtown/Trashtown_P',
        '/Game/Maps/ProvingGrounds/Trial1/ProvingGrounds_Trial1_P',
        '/Game/Maps/ProvingGrounds/Trial4/ProvingGrounds_Trial4_P',
        '/Game/Maps/ProvingGrounds/Trial5/ProvingGrounds_Trial5_P',
        '/Game/Maps/ProvingGrounds/Trial6/ProvingGrounds_Trial6_P',
        '/Game/Maps/ProvingGrounds/Trial7/ProvingGrounds_Trial7_P',
        '/Game/Maps/ProvingGrounds/Trial8/ProvingGrounds_Trial8_P',
        '/Game/Maps/Sanctuary3/Sanctuary3_P',
        '/Game/Maps/Slaughters/COVSlaughter/COVSlaughter_P',
        '/Game/Maps/Slaughters/CreatureSlaughter/CreatureSlaughter_P',
        '/Game/Maps/Slaughters/TechSlaughter/TechSlaughter_P',
        '/Game/Maps/Zone_0/FinalBoss/FinalBoss_P',
        '/Game/Maps/Zone_0/Prologue/Prologue_P',
        '/Game/Maps/Zone_0/Recruitment/Recruitment_P',
        '/Game/Maps/Zone_0/Sacrifice/Sacrifice_P',
        '/Game/Maps/Zone_1/AtlasHQ/AtlasHQ_P',
        '/Game/Maps/Zone_1/City/City_P',
        '/Game/Maps/Zone_1/CityBoss/CityBoss_P',
        '/Game/Maps/Zone_1/CityVault/CityVault_P',
        '/Game/Maps/Zone_1/Monastery/Monastery_P',
        '/Game/Maps/Zone_1/OrbitalPlatform/OrbitalPlatform_P',
        '/Game/Maps/Zone_1/Outskirts/Outskirts_P',
        '/Game/Maps/Zone_1/Towers/Towers_P',
        '/Game/Maps/Zone_2/Mansion/Mansion_P',
        '/Game/Maps/Zone_2/MarshFields/MarshFields_P',
        '/Game/Maps/Zone_2/Prison/Prison_P',
        '/Game/Maps/Zone_2/Watership/Watership_P',
        '/Game/Maps/Zone_2/Wetlands/Wetlands_P',
        '/Game/Maps/Zone_2/WetlandsBoss/WetlandsBoss_P',
        '/Game/Maps/Zone_2/WetlandsVault/WetlandsVault_P',
        '/Game/Maps/Zone_3/Convoy/Convoy_P',
        '/Game/Maps/Zone_3/Desert/Desert_P',
        '/Game/Maps/Zone_3/DesertBoss/DesertBoss_P',
        '/Game/Maps/Zone_3/DesertVault/Desertvault_P',
        '/Game/Maps/Zone_3/Mine/Mine_P',
        '/Game/Maps/Zone_3/Motorcade/Motorcade_P',
        '/Game/Maps/Zone_3/MotorcadeFestival/MotorcadeFestival_P',
        '/Game/Maps/Zone_3/MotorcadeInterior/MotorcadeInterior_P',
        '/Game/Maps/Zone_4/Beach/Beach_P',
        '/Game/Maps/Zone_4/Crypt/Crypt_P',
        '/Game/Maps/Zone_4/Desolate/Desolate_P',
        '/Game/PatchDLC/BloodyHarvest/Maps/Seasons/BloodyHarvest/BloodyHarvest_P',
        '/Game/PatchDLC/Event2/Maps/Cartels_P',
        '/Game/PatchDLC/Raid1/Maps/Raid/Raid_P',
        '/Game/PatchDLC/Takedown2/Maps/GuardianTakedown_P',
        '/Geranium/Maps/CraterBoss/CraterBoss_P',
        '/Geranium/Maps/Facility/Facility_P',
        '/Geranium/Maps/Forest/Forest_P',
        '/Geranium/Maps/Frontier/Frontier_P',
        '/Geranium/Maps/Lodge/Lodge_P',
        '/Geranium/Maps/Town/Town_P',
        '/Hibiscus/Maps/Archive/Archive_P',
        '/Hibiscus/Maps/Bar/Bar_P',
        '/Hibiscus/Maps/Camp/Camp_P',
        '/Hibiscus/Maps/Lake/Lake_P',
        '/Hibiscus/Maps/Venue/Venue_P',
        '/Hibiscus/Maps/Village/Village_P',
        '/Hibiscus/Maps/Woods/Woods_P',
        '/Ixora/Maps/FrostSite/FrostSite_P',
        '/Ixora2/Maps/Boss/SacrificeBoss_p',
        '/Ixora2/Maps/Cabin/Cabin_P',
        '/Ixora2/Maps/Mystery/Nekro/NekroMystery_p',
        '/Ixora2/Maps/Mystery/Pandora/PandoraMystery_p',
        '/Ixora2/Maps/Noir/Noir_P',
        ]:
    level_short = level_full.rsplit('/', 1)[-1]
    level_label = LVL_TO_ENG_LOWER[level_short.lower()]
    mod.comment(level_label)
    chest_name = mod.streaming_hotfix(level_full,
            '/Game/PatchDLC/VaultCard/InteractiveObjects/BPIO_Lootable_VaultCard_RedCrate',
            location=(99999,99999,99999),
            )
    mod.reg_hotfix(Mod.LEVEL, level_short,
            chest_name,
            'OpeningInteractions.OpeningInteractions[0].TransitionAnimation',
            Mod.get_full_cond('/Game/PatchDLC/VaultCard/AS_Open_v2', 'AnimSequence'),
            )
    mod.newline()

class AS():

    def __init__(self, path, scale=None, seqlen_scale=None, extra_char=None, method=Mod.LEVEL):
        self.path = path
        self.scale = scale
        self.seqlen_scale = seqlen_scale
        self.extra_char = extra_char
        self.method = method

    def _do_scale(self, mod, data, hf_trigger, hf_target):
        """
        Method to shorten animation sequences
        """

        # Serialize the data
        as_data = data.get_exports(self.path, 'AnimSequence')[0]

        # First the RateScale; happens regardless of AnimSequence contents
        mod.reg_hotfix(hf_trigger, hf_target,
                self.path,
                'RateScale',
                self.scale)

        # Now Notifies
        if 'Notifies' in as_data:
            for idx, notify in enumerate(as_data['Notifies']):
                for var in ['SegmentBeginTime', 'SegmentLength', 'LinkValue']:
                    if var in notify and notify[var] != 0:
                        mod.reg_hotfix(hf_trigger, hf_target,
                                self.path,
                                'Notifies.Notifies[{}].{}'.format(idx, var),
                                round(notify[var]/self.scale, 6))

                # If we have targets inside EndLink, process that, too.  (So far, it doesn't
                # look like any animations we touch actually have anything here.)
                endlink = notify['EndLink']
                if 'export' not in endlink['LinkedMontage'] \
                        or endlink['LinkedMontage']['export'] != 0 \
                        or 'export' not in endlink['LinkedSequence'] \
                        or endlink['LinkedSequence']['export'] != 0:
                    for var in ['SegmentBeginTime', 'SegmentLength', 'LinkValue']:
                        if var in endlink and endlink[var] != 0:
                            mod.reg_hotfix(hf_trigger, hf_target,
                                    self.path,
                                    'Notifies.Notifies[{}].EndLink.{}'.format(idx, var),
                                    round(endlink[var]/self.scale, 6))

        # Finally: SequenceLength.  This one's a bit weird, which is why we're letting categories
        # decide if they want to use alt scalings.  For player animations for entering/leaving vehicles
        # (or for changing seats), if SequenceLength is scaled at the same scale as the rest of the
        # animations, the animation "freezes" before it's fully complete, and the player just jerks
        # to their final spot once the appropriate time has elapsed.  Contrariwise, if we *don't*
        # scale SequenceLength down, you end up with a period of time where you can't interact with
        # the vehicle at all, like driving, leaving, or changing seats again.  In the end, I settled
        # on just using the global vehicle scale for all categories here, but if I want to tweak
        # something in the future, at least it's easy enough to do so.
        if 'SequenceLength' in as_data:
            mod.reg_hotfix(hf_trigger, hf_target,
                    self.path,
                    'SequenceLength',
                    round(as_data['SequenceLength']/self.seqlen_scale, 6))

    def do_scale(self, mod, data):
        if self.method == Mod.PATCH:
            target = ''
        elif self.method == Mod.LEVEL or self.method == Mod.CHAR:
            target = 'MatchAll'
        else:
            raise RuntimeError(f'Unknown method for AnimSequence patching: {self.method}')
        self._do_scale(mod, data, self.method, target)
        if self.extra_char:
            self._do_scale(mod, data, Mod.CHAR, self.extra_char)

# Direct animation speedups
mod.header('Simple Animation Speedups')
for cat_name, cat_scale, animseqs in [
        ('Containers', global_scale, [
            # Initial object list generated by:
            #     find $(find . -type d -name Lootables) -name "AS_*.uasset" | sort -i | cut -d. -f2 | grep -vE '(Idle|Flinch|_Closed|_Opened)'
            # ... while at the root of a data unpack
            AS('/Alisma/Lootables/Hyperion/AmmoCase/Animation/AS_Open_In'),
            AS('/Alisma/Lootables/Hyperion/LootCase/Animation/AS_Hyp_Misc2_Opening'),
            AS('/Alisma/Lootables/Hyperion/PortaPotty/Animation/AS_Open_IN_Poor'),
            AS('/Alisma/Lootables/Hyperion/PortaPotty/Animation/AS_Open_IN'),
            AS('/Alisma/Lootables/Hyperion/PortaPotty/Animation/AS_Open'),
            AS('/Alisma/Lootables/Hyperion/RedChest/Animation/AS_HypRedChest_Open'),
            AS('/Alisma/Lootables/Hyperion/SingleCase/Animation/AS_SingleCase_In'),
            AS('/Alisma/Lootables/Hyperion/WeaponBox/Animation/AS_HypWeaponLocker_Open'),
            AS('/Dandelion/Lootables/Hyperion/AmmoCase/Animation/AS_Open_In'),
            AS('/Dandelion/Lootables/Hyperion/BlackJackChest/Animation/AS_Open_Draw_card_01'),
            AS('/Dandelion/Lootables/Hyperion/BlackJackChest/Animation/AS_Open_Draw_card_03'),
            AS('/Dandelion/Lootables/Hyperion/BlackJackChest/Animation/AS_Open_Draw_card_04'),
            AS('/Dandelion/Lootables/Hyperion/BlackJackChest/Animation/AS_Open_In'),
            AS('/Dandelion/Lootables/Hyperion/LootCase/Animation/AS_Hyp_Misc2_Opening'),
            AS('/Dandelion/Lootables/Hyperion/PortaPotty/Animation/AS_Open_IN'),
            AS('/Dandelion/Lootables/Hyperion/RedChest/Animation/AS_HypRedChest_Open'),
            AS('/Dandelion/Lootables/Hyperion/SingleCase/Animation/AS_SingleCase_In'),
            AS('/Dandelion/Lootables/Hyperion/WeaponBox/Animation/AS_HypWeaponLocker_Open'),
            AS('/Game/Lootables/Atlas/Chest_Red/Animation/AS_Open'),
            AS('/Game/Lootables/Atlas/Crate_Ammo/Animation/AS_Open'),
            AS('/Game/Lootables/COV/Bandit_CardboardBox/Animation/AS_Open_Fast'),
            AS('/Game/Lootables/COV/Bandit_CardboardBox/Animation/AS_Open_Slow'),
            AS('/Game/Lootables/COV/Chest_Red/Animation/AS_Open_v1'),
            AS('/Game/Lootables/COV/Chest_White/Animations/AS_Open'),
            AS('/Game/Lootables/COV/Crate_Ammo/Animation/AS_Open_v1'),
            AS('/Game/Lootables/COV/Crate_OfferingBox/Animation/AS_Open_v1'),
            AS('/Game/Lootables/Eridian/Chest_Red/Animation/AS_Open'),
            AS('/Game/Lootables/Eridian/Chest_White/Animation/AS_Open'),
            AS('/Game/Lootables/Eridian/Crate_Ammo/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Gold/Animation/AS_Close'),
            AS('/Game/Lootables/_Global/Chest_Gold/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Trials/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Chest_Trials/Animation/AS_Open_v2'),
            AS('/Game/Lootables/_Global/Chest_Typhon/Animation/AS_Open',
                # Typhon Dead Drop doesn't seem to actually apply with just a Level hotfix.  I
                # suspect it gets loaded in too late, or something?  Anyway, applying a Char
                # hotfix instead seems to do the trick, so whatever.
                extra_char='MatchAll',
                ),
            AS('/Game/Lootables/_Global/Crate_Ammo/Animations/AS_Open'),
            AS('/Game/Lootables/_Global/Dumpster_Small/Animation/AS_Open'),
            AS('/Game/Lootables/_Global/Locker_Generic/Animation/AS_Open_Misnamed'),
            AS('/Game/Lootables/_Global/Locker_Generic/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Cash_Register/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Lock_Box/Animations/AS_Open'),
            AS('/Game/Lootables/Industrial/Machine_Washing/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/PortaPotty/Animation/AS_BlastOff'),
            AS('/Game/Lootables/Industrial/PortaPotty/Animation/AS_Open_v1'),
            AS('/Game/Lootables/Industrial/Refrigerator/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Safe/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Strong_Box/Animation/AS_Open'),
            AS('/Game/Lootables/Industrial/Toilet/Animations/AS_Open'),
            AS('/Game/Lootables/Industrial/Trunk_Car/Animation/AS_Open_Backfire'),
            AS('/Game/Lootables/Industrial/Trunk_Car/Animation/AS_Open'),
            AS('/Game/Lootables/Jakobs/Chest_Red/Animation/AS_Open'),
            AS('/Game/Lootables/Jakobs/Chest_White/Animation/AS_Open'),
            AS('/Game/Lootables/Jakobs/GunRack/Animation/AS_Open'),
            AS('/Game/Lootables/Jakobs/Lockbox/Animation/AS_Open'),
            AS('/Game/Lootables/Jakobs/MusicBox/Animation/AS_Open'),
            AS('/Game/Lootables/Maliwan/Ammo/Animation/AS_Open_v1'),
            AS('/Game/Lootables/Maliwan/Chest_Red/Animation/AS_Open'),
            AS('/Game/Lootables/Maliwan/Chest_White/Animation/AS_Open'),
            AS('/Game/Lootables/Mission_Specific/Rock_HideAKey/Animation/AS_Open'),
            AS('/Game/Lootables/Pandora/Mailbox/Animation/AS_Open_v1'),
            AS('/Game/Lootables/Pandora/Mailbox/Animation/AS_Open_v2'),
            AS('/Game/Lootables/Pandora/TrashCan/Model/Animation/AS_Open_v1'),
            AS('/Game/Lootables/Pandora/TrashCan/Model/Animation/AS_Open_v2'),
            # This one doesn't show up in the find command above...
            AS('/Game/Lootables/Pandora/TrashCan/Model/Animation/Open_v3'),
            AS('/Game/Lootables/Pandora/Varkid_Lootable/_Shared/Animation/AS_Open_Burst'),
            AS('/Game/Lootables/Pandora/Varkid_Lootable/_Shared/Animation/AS_Open'),
            AS('/Game/Lootables/Promethea/Cooler/Animation/AS_Open'),
            AS('/Game/Lootables/Promethea/Gashapon/Animations/AS_Open'),
            AS('/Game/Lootables/Promethea/Ratch_pile/Animation/Ratch_Pile_Large/AS_Open'),
            AS('/Game/Lootables/Promethea/Ratch_pile/Animation/Ratch_Pile_Large_Open/AS_Open'),
            AS('/Game/Lootables/Promethea/Ratch_pile/Animation/Ratch_Pile_Small/AS_Open'),
            AS('/Game/Lootables/Promethea/Ratch_pile/Animation/Ratch_Pile_Small_Open/AS_Open'),
            AS('/Game/Lootables/Promethea/Toilet/Animation/AS_Open_v1'),
            # Make this one not *quite* as fast as the rest.  Also requires the injection
            # above this, otherwise this object won't exist yet.
            AS('/Game/PatchDLC/VaultCard/AS_Open_v2',
                    scale=2,
                    seqlen_scale=2,
                    ),
            AS('/Geranium/Lootables/CashRegister/Animation/AS_Open'),
            AS('/Geranium/Lootables/Chest_DeadDrop/Model/Anims/AS_Open_Ger'),
            AS('/Geranium/Lootables/_Design/Classes/AS_Open_MoneyBack'),
            AS('/Geranium/Lootables/Machine_Washing/Animation/AS_Close'),
            AS('/Geranium/Lootables/Outhouse/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/Carcass/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/Cultists/AmmoCrate/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/Cultists/RedChest/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/Cultists/UniqueChest/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/Cultists/WhiteChest/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/FishingNet/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/FrostBiters/AmmoCrate/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/FrostBiters/RedChest/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/FrostBiters/TreasureBox/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/FrostBiters/WhiteChest/Animation/AS_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/SingingFish/Animation/AS_Sing_Sing'),
            AS('/Hibiscus/InteractiveObjects/Lootables/SingingFish/Animation/AS_Sing_Spit'),
            AS('/Hibiscus/InteractiveObjects/Lootables/SingleMushroom/AS_Mush_Open'),
            AS('/Hibiscus/InteractiveObjects/Lootables/TentacleToilet/Animation/AS_TentacleToilet_OpenAndDropWeapon'),
            ]),
        ('Doors', door_scale, [
            # Called by IO_Door_1000x600_SlideUp_Promethea_Vehicle2, the door to the hub area in City_P,
            # and also before the big pit in OrbitalPlatform_P (after the thruster).  We're doing some
            # custom sequence scaling here 'cause in OrbitalPlatform_P, if we leave the animsequence
            # scaling at the default, the door animation freezes *right* at the beginning and doesn't
            # open hardly at all.  Leaving the sequence scale at 1 lets that work fine though, and the
            # animation is still sped up, so that should do for now.  It does make me wonder if we maybe
            # shouldn't be touching that value *at all*, but I guess I'll leave it for now.
            AS('/Game/InteractiveObjects/Doors/Eden_6/Door_Eden6_VehicleSpawner/Animation/AS_VehicleDoor_Open',
                seqlen_scale=1,
                ),
            ]),
        # Doing this ends up screwing up the slots pretty thoroughly, actually -- the animation gets killed
        # pretty much immediately, so the rewards get stuck "inside" the machine until the 10-sec auto-drop
        # timer elapses.  Weird.  Anyway, the drawer animations aren't awful anyway, so just leave 'em.
        #('Slot Machine Components', global_scale, [
        #    '/Game/InteractiveObjects/GameSystemMachines/SlotMachine/Animation/AS_SlotMachine_Drawer_Close',
        #    '/Game/InteractiveObjects/GameSystemMachines/SlotMachine/Animation/AS_SlotMachine_Drawer_Open',
        #    '/Game/InteractiveObjects/GameSystemMachines/SlotMachine/Animation/AS_Slotmachine_Locker_Closing',
        #    '/Game/InteractiveObjects/GameSystemMachines/SlotMachine/Animation/AS_Slotmachine_Locker_Opening',
        #    ]),
        ('Character Death Respawns', global_scale, [
            # Turns out this affects the *entire* respawn sequence, including digistruct tunnel.
            # At our current rates, it ends up basically omitting the char-standing-up animation
            # entirely.  (And also the char doesn't end up facing the right way 'cause the camera
            # doesn't go through its motions.  Whatever.)
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/FFYL/AS_Respawn_Kneel'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/FFYL/AS_Respawn_Kneel'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/FFYL/AS_Respawn_Kneel'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/FFYL/AS_Respawn_Kneel'),
            ]),
        ('NPC Animations', 2, [
            AS('/Game/NonPlayerCharacters/Ava/Animation/Missions/AS_MayaDeathReaction_Enter'),
            AS('/Game/NonPlayerCharacters/Ava/Animation/Missions/AS_MayaDeathReaction_Exit'),
            AS('/Game/Enemies/Saurian/_Shared/Animation/Missions/AS_FastDigging'),
            ]),
        ]:

    mod.comment(cat_name)

    for animseq in animseqs:

        if animseq.scale is None:
            animseq.scale = cat_scale
        if animseq.seqlen_scale is None:
            animseq.seqlen_scale = animseq.scale

        animseq.do_scale(mod, data)

    mod.newline()

mod.header('Extra Container Tweaks')

# Maliwan Ammo Crate Digistructs
mod.comment('Maliwan Ammo Crate Digistructs')
# Honestly not sure what exactly this controls, though it's *not* anything to do with the animation trigger
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/Lootables/_Design/Classes/Maliwan/BPIO_Lootable_Maliwan_AmmoCrate.BPIO_Lootable_Maliwan_AmmoCrate_C:Loot_GEN_VARIABLE',
        'AutoLootDelayOverride',
        0.8/global_scale)
# This is the delay for the "light burst" effect, and maybe when the digistruct animation
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/GameData/Loot/CoordinatedEffects/BP_CE_Maliwan_Loot_Digistruct_In.Default__BP_CE_Maliwan_Loot_Digistruct_In_C',
        'ParticleEffects.ParticleEffects[0].StartTime',
        0.25/global_scale)
# *this* is what speeds up the actual digistruct animation on the individual items
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/GameData/Loot/CoordinatedEffects/BP_CE_Maliwan_Loot_Digistruct_In.Default__BP_CE_Maliwan_Loot_Digistruct_In_C',
        'Duration',
        round(2.1/global_scale, 6))
mod.newline()

# Eridian ammo crate light-burst speedup
# This doesn't actually affect anything important, but the animation as-is makes the crate-opening
# *look* slower, so I'm tweaking it anyway.  Note that this doesn't really speed it up as much
# as it should; this ends up resulting in maybe a 2x speedup instead of our 4x intended.  So there's
# still something going on, but whatever, it's better.
mod.comment('Eridian Ammo Crate Light-Burst Speedup')
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/Lootables/Eridian/Chest_Red/Effects/Systems/PS_Eridian_Ammo_Chest_SinkNBurn',
        'Emitters.Emitters[1].Object..LODLevels.LODLevels[0].Object..TypeDataModule..Object..EmitterInfo.MaxLifetime',
        2/global_scale)
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/Lootables/Eridian/Chest_Red/Effects/Systems/PS_Eridian_Ammo_Chest_SinkNBurn',
        'Emitters.Emitters[1].Object..LODLevels.LODLevels[0].Object..Modules.Modules[0].Object..Lifetime.MinValue',
        2/global_scale)
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/Lootables/Eridian/Chest_Red/Effects/Systems/PS_Eridian_Ammo_Chest_SinkNBurn',
        'Emitters.Emitters[1].Object..LODLevels.LODLevels[0].Object..Modules.Modules[0].Object..Lifetime.MaxValue',
        2/global_scale)
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/Lootables/Eridian/Chest_Red/Effects/Systems/PS_Eridian_Ammo_Chest_SinkNBurn',
        'Emitters.Emitters[1].Object..LODLevels.LODLevels[0].Object..Modules.Modules[0].Object..Lifetime.Table.Values.Values[0]',
        2/global_scale)
mod.newline()

mod.header('Eridian Tools')

for anim_obj in [
        '/PlayerCharacters/_Shared/Animation/Skills/VaultRewards/1st/AS_Analyzer_Use',
        '/PlayerCharacters/_Shared/Animation/Skills/VaultRewards/1st/AS_Eridian_Melee_Small',
        '/PlayerCharacters/_Shared/Animation/Skills/VaultRewards/1st/Eridian_Analyzer/AS_Analyzer_Use',
        '/PlayerCharacters/Beastmaster/_Shared/Animation/Skills/VaultRewards/3rd/AS_Analyzer_Use',
        '/PlayerCharacters/Beastmaster/_Shared/Animation/Skills/VaultRewards/3rd/AS_Eridian_Melee_Small',
        '/PlayerCharacters/Gunner/_Shared/Animation/Skills/VaultRewards/3rd/AS_Analyzer_Use',
        '/PlayerCharacters/Gunner/_Shared/Animation/Skills/VaultRewards/3rd/AS_Eridian_Melee_Small',
        '/PlayerCharacters/Operative/_Shared/Animation/Skills/VaultRewards/3rd/AS_Analyzer_Use',
        '/PlayerCharacters/Operative/_Shared/Animation/Skills/VaultRewards/3rd/AS_Eridian_Melee_Small',
        '/PlayerCharacters/SirenBrawler/_Shared/Animation/Skills/VaultRewards/3rd/AS_Analyzer_Use',
        '/PlayerCharacters/SirenBrawler/_Shared/Animation/Skills/VaultRewards/3rd/AS_Eridian_Melee_Small',
        ]:

    mod.reg_hotfix(Mod.PATCH, '',
            anim_obj,
            'RateScale',
            global_eridian_scale)

mod.newline()

# Vehicles!
#
# Command for these: find $(find . -name Vehicles -o -name Vehicle) -name "AS_*.uasset" | sort -i | cut -d. -f2 | grep -vE '(Idle|Flinch|Death|Land|Emperor)'
# ... though it's been trimmed quite heavily and reorganized quite a bit.
for vehicle_cat, hf_trigger, vehicle_scale, sequencelength_scale, animseqs in [
        ('Player Basic Interactions (always loaded objects)', Mod.PATCH, global_vehicle_scale, global_vehicle_scale, [
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/CraneConsole/AS_Console_Enter'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/CraneConsole/AS_Console_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Entry'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_R'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Exit'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Shared/AS_Base_Pose'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/CraneConsole/AS_Console_Enter'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/CraneConsole/AS_Console_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Entry'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_R'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Exit'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Shared/AS_Base_Pose'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/CraneConsole/AS_Console_Enter'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/CraneConsole/AS_Console_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Entry'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_R'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Exit'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Shared/AS_Base_Pose'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Crane/AS_Console_Enter'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Crane/AS_Console_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Entry'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/GunnersNest/AS_GunnersNest_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Standing_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_Exit_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Turret_to_Driver'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_Exit_R'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Enter_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/RollerCoaster/AS_RollerCoaster_Exit'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Shared/AS_Base_Pose'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_BL_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_BR_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_to_Turret'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel_Backward'),
            #AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Driver_TurnWheel'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_Exit'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Turret_to_Driver'),
            ]),
        ('Player Basic Interactions (level-based objects)', Mod.LEVEL, global_vehicle_scale, global_vehicle_scale, [
            AS('/Dandelion/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Hyperhoop/AS_Hyperhoop_Enter'),
            AS('/Dandelion/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Hyperhoop/AS_Hyperhoop_Exit'),
            AS('/Dandelion/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Hyperhoop/AS_Hyperhoop_Enter'),
            AS('/Dandelion/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Hyperhoop/AS_Hyperhoop_Exit'),
            AS('/Dandelion/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Hyperhoop/AS_Hyperhoop_Enter'),
            AS('/Dandelion/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Hyperhoop/AS_Hyperhoop_Exit'),
            AS('/Dandelion/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicle/Hyperhoop/AS_Hyperhoop_Enter'),
            AS('/Dandelion/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicle/Hyperhoop/AS_Hyperhoop_Exit'),
            #AS('/Dandelion/Vehicles/Hyperloop/Animation/AS_Banking_Left'),
            #AS('/Dandelion/Vehicles/Hyperloop/Animation/AS_Banking_Right'),
            ]),
        ('Hijack Interactions - Player', Mod.PATCH, global_vehicle_scale, global_vehicle_scale, [
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Standing'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Hijack_Driver_L'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Revolver/AS_Hijack_Driver_R'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/Beastmaster/_Shared/Animation/Generic/Vehicles/Technical/AS_Hijack_Driver'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Standing'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_HiJack_Driver_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_HiJack_Driver_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_HiJack_Driver_L'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Revolver/AS_HiJack_Driver_R'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/Gunner/_Shared/Animation/Generic/Vehicles/Technical/AS_HiJack_Driver'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Standing'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_HiJack_Driver_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Hijack_Driver_L'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Revolver/AS_Hijack_Driver_R'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/Operative/_Shared/Animation/Generic/Vehicles/Technical/AS_HiJack_Driver'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Sitting_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/MannedTurret/AS_Hijack_Standing'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_HiJack_Driver_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_HiJack_Driver_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Outrunner/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_HiJack_Driver_L'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Revolver/AS_HiJack_Driver_R'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_Hijack_Driver_to_Turret'),
            AS('/Game/PlayerCharacters/SirenBrawler/_Shared/Animation/Generic/Vehicles/Technical/AS_HiJack_Driver'),
            ]),
        ('NPC Basic Interactions', Mod.CHAR, global_vehicle_scale, global_vehicle_scale, [
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Enter_L'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Exit_L'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Exit_R'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapB_Attack'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapB_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapB_Unstable'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapF_Attack'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapF_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapF_Unstable'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Enter_L'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Revolver/AS_Driver_Enter_L'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Revolver/AS_Driver_Exit_L'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Revolver/AS_Driver_TurnWheel'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_Base_Pose'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_VehicleLeap_Enter'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_BL_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_BR_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Driver_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Driver_TurnWheel'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFL_Attack'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFL_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFL_Unstable'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFR_Attack'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFR_Exit'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFR_Unstable'),
            #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Turret_Exit'),
            #AS('/Game/Enemies/Punk_Male/_Shared/Animation/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/Enemies/Punk_Male/_Shared/Animation/Vehicles/Technical/AS_BL_Exit'),
            #AS('/Game/Enemies/Punk_Male/_Shared/Animation/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/Enemies/Punk_Male/_Shared/Animation/Vehicles/Technical/AS_BR_Exit'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Exit'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Enter_L'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Exit_L'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Enter_L'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Exit'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_Driver_Enter_L'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_Driver_Exit_L'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_Driver_Exit_R'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_Driver_TurnWheel'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Shared/AS_Base_Pose'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_BL_Exit'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_BR_Exit'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Driver_Exit'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Driver_TurnWheel'),
            #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Turret_Exit'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/MannedTurret/AS_Standing_Exit'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Shared/AS_Base_Pose'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_BL_Exit'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_BR_Exit'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_Driver_Exit'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_Driver_TurnWheel'),
            #AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/NonPlayerCharacters/AtlasSoldier/Animation/Vehicles/Technical/AS_Turret_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_L'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Enter_R'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_L'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Exit_R'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Enter_L'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Enter_R'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Driver_Exit_L'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Driver_TurnWheel'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Enter_L'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Enter_R'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Revolver/AS_Driver_Enter_L'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Revolver/AS_Driver_Enter_R'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Revolver/AS_Driver_Exit_L'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Revolver/AS_Driver_TurnWheel'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Shared/AS_Base_Pose'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_AllyDriver_Brace'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_AllyDriver_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_AllyDriver_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_BL_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_BL_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_BR_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_BR_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_Driver_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_Driver_Exit'),
            #AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_Driver_TurnWheel'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_Turret_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/AS_Turret_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/Passive/AS_BL_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/Passive/AS_BL_Exit'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/Passive/AS_BR_Enter'),
            AS('/Game/NonPlayerCharacters/_Generic/_Shared/Animation/Vehicles/Technical/Passive/AS_BR_Exit'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Revolver/AS_Driver_Enter_L'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Revolver/AS_Driver_Enter_R'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Revolver/AS_Driver_Exit_L'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Revolver/AS_Driver_TurnWheel'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/NonPlayerCharacters/Lilith/Animation/Vehicles/Shared/AS_Base_Pose'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Shared/AS_ADD_FB'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Shared/AS_ADD_LR'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Shared/AS_ADD_UD'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Shared/AS_AllyPassenger_BasePose'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_Attack'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_CC'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_CD'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_CU'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_LC'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_LD'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_LU'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_RC'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_RD'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_AO_RU'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_BackLeft_Attack'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_Brace'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_Charge_In'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_Enter'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_Exit'),
            #AS('/Game/NonPlayerCharacters/Maya/Animation/Vehicle/Technical/AS_AllyPassenger_Shield'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Shared/AS_ADD_FB'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Shared/AS_ADD_LR'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Shared/AS_ADD_UD'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Shared/AS_AllyPassenger_BasePose'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Technical/AS_AllyDriver_Brace'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Technical/AS_AllyDriver_Enter'),
            #AS('/Game/NonPlayerCharacters/Vaughn/Animation/Vehicles/Technical/AS_AllyDriver_Exit'),
            ]),
        ('Hijack Interactions - Enemies', Mod.CHAR, global_vehicle_scale, global_vehicle_scale, [
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Hijack_Sitting_L'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Hijack_Sitting_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Hijack_Standing'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_HiJack_Driver_L'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_HiJack_Driver_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Hijack_Driver_to_Turret'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Revolver/AS_Hijack_Driver_L'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Revolver/AS_Hijack_Driver_R'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_HiJacked_Ejected'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Hijack_Driver_to_Turret'),
            AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Hijack_Driver'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Hijack_Sitting_L'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Hijack_Sitting_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Hijack_Standing'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_HiJack_Driver_L'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_HiJack_Driver_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Hijack_Driver_to_Turret'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_HiJack_Driver_L'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Revolver/AS_HiJack_Driver_R'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Hijack_Driver_to_Turret'),
            AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_HiJack_Driver'),
            ]),
        #('Other (unused, currently)', Mod.LEVEL, global_vehicle_scale, global_vehicle_scale, [
        #    AS('/Game/Vehicles/Carnivora/Animation/AS_Entry_drop'),
        #    AS('/Game/Vehicles/Carnivora/Animation/AS_Entry_idle'),
        #    AS('/Game/Vehicles/Carnivora/Animation/AS_Magnet_Drop'),
        #    AS('/Game/Vehicles/Outrunner/Animation/AS_Outrunner_GearShift_Down'),
        #    AS('/Game/Vehicles/Outrunner/Animation/AS_Outrunner_GearShift_Up'),
        #    AS('/Game/Vehicles/Outrunner/Animation/AS_Vehicle_Spawn_DoorCargoSplit'),
        #    AS('/Game/Vehicles/Revolver/Animation/AS_Gunner_Enter_L'),
        #    AS('/Game/Vehicles/Revolver/Animation/AS_Gunner_Exit_L'),
        #    AS('/Game/Vehicles/Revolver/Animation/AS_Revolver_GearShift_Down'),
        #    AS('/Game/Vehicles/Revolver/Animation/AS_Revolver_GearShift_Up'),
        #    AS('/Game/Vehicles/Revolver/Animation/AS_Vehicle_Spawn_DoorCargoSplit'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_BrakeBounce_B'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_BrakeBounce_F'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_GearShift_Down'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_GearShift_Up'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_Gunner_Driver_Enter'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_Gunner_Driver_Exit'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Technical_Hit_HoodDown'),
        #    AS('/Game/Vehicles/Technical/Animation/AS_Vehicle_Spawn_DoorCargoSplit'),
        #    AS('/Game/Vehicles/Technical/Parts/JetBooster/AS_JetBooster_Anim'),
        #    AS('/Game/Vehicles/Technical/Parts/MeatGrinder/AS_Veh_Techincal_MeatGrinder'),
        #    AS('/Game/Vehicles/Technical/Parts/ToxicBooster/AS_Veh_Technical_ToxicBooster'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/BouncingLasers/AS_BouncingLasers_Shoot'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/Catapult/AS_Launch'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/Catapult_TireBombs/AS_Launch'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/DualFlakCanon/AS_Veh_Turret_DualFlakCanon_Shoot_Primary'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/HeavyMissile/AS_HeavyMissile_Shoot'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/MachineGun/AS_MachineGun_Shoot_Heavy'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/MachineGun/AS_MachineGun_Shoot'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/PulseRifle/Animation/AS_PulseRifle_DualTurrets_Deploy_In'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/PulseRifle/Animation/AS_PulseRifle_DualTurrets_Deploy_Out'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/PulseRifle/Animation/AS_PulseRifle_DualTurrets_Retracted'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/PulseRifle/Animation/AS_PulseRifle_Shoot'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/RodLauncher/AS_Veh_Turret_RodLauncher_Shoot_Primary'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/SawBlade/AS_Veh_Turret_SawBlade_Shoot_Primary'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/ShotgunMissile/AS_ShotgunMissile_Shoot'),
        #    AS('/Game/Vehicles/VehicleWeapons/_Shared/WeaponModels/SwarmerMissile/AS_SwarmerMissile_Shoot'),
        #    AS('/Geranium/NonPlayerCharacters/Dakota/Animation/Vehicles/JetBeast/AS_Driver_Exit_L'),
        #    AS('/Geranium/Vehicles/Horse/Animation/Cannon/AS_Fire'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapB_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_LeapF_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Idle'),
        #    #AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_ADD_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Shared/AS_VehicleLeap_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFL_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_LeapFR_Idle'),
        #    AS('/Game/Enemies/Psycho_Male/_Shared/Animation/Vehicles/Technical/AS_Turret_Idle'),
        #    AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Sitting_Idle'),
        #    AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/MannedTurret/AS_Standing_Idle'),
        #    AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Outrunner/AS_Turret_Idle'),
        #    #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Shared/AS_ADD_Idle'),
        #    #AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_BL_Idle'),
        #    AS('/Game/Enemies/Trooper/_Shared/Animation/Vehicles/Technical/AS_Turret_Idle'),
        #    ]),
        ]:

    mod.header('Vehicle Speedups: {}'.format(vehicle_cat))

    for animseq in animseqs:

        if verbose:
            print('Processing {}'.format(animseq.path))

        animseq.method = hf_trigger
        animseq.scale = vehicle_scale
        animseq.seqlen_scale = sequencelength_scale

        mod.comment(animseq.path)
        animseq.do_scale(mod, data)
        mod.newline()

# Default here is 2.36; not gonna bother dynamically reading it for a single object.
# This honestly doesn't really do much for you -- the vehicle is basically fully
# operable as soon as it starts, anyway.  Still, it makes things look a little
# snappier.
mod.header('Catch-A-Ride Digistruct Time')
mod.reg_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/GameData/StatusEffects/CoordinatedEffects/Vehicles/BP_CE_Veh_Digistruct_In.Default__BP_CE_Veh_Digistruct_In_C',
        'Duration',
        0.5)
mod.newline()

class IO():

    def __init__(self, path, label=None, level='MatchAll', scale=None):
        self.path = path
        self.last_bit = path.split('/')[-1]
        self.last_bit_c = f'{self.last_bit}_C'
        self.full_path = f'{self.path}.{self.last_bit_c}'
        if label is None:
            self.label = self.last_bit
        else:
            self.label = label
        self.level = level
        self.scale = scale

checked_ver = False
for category, cat_scale, io_objs in [
        ('Doors', door_scale, [
            # find $(find . -name Doors) -name "IO_*.uasset" | sort -i | cut -d. -f2 | grep -v Parent
            IO('/Alisma/InteractiveObjects/General/Doors/IO_Door_130x250_SlideLeft_Hyperion'),
            IO('/Alisma/InteractiveObjects/General/Doors/IO_Door_130x250_SlideUp_Prison'),
            IO('/Alisma/InteractiveObjects/General/Doors/IO_Door_400x400_SlideDown_Hyp'),
            IO('/Alisma/InteractiveObjects/General/Doors/IO_DoubleDoor_SlideUp_Hyp'),
            # This one's just part of a cutscene; stays open otherwise
            #IO('/Dandelion/InteractiveObjects/Doors/IO_Door_800x600_SlideUp_TrashTownMainEntry'),
            IO('/Dandelion/InteractiveObjects/Doors/IO_Door_Hyperion_DoubleGlass'),
            IO('/Dandelion/InteractiveObjects/Doors/IO_Door_Hyperion_Double'),
            IO('/Dandelion/InteractiveObjects/Doors/IO_Door_Hyperion_Single_TricksyNickLoot'),
            IO('/Dandelion/InteractiveObjects/Doors/IO_Door_Hyperion_Single'),
            # No timing parameters on these two
            #IO('/Dandelion/InteractiveObjects/Doors/PrizeDoors/IO_Door_Hyperion_Single_Prize'),
            #IO('/Dandelion/InteractiveObjects/Doors/PrizeDoors/IO_Switch_Hyp_Button_V1_Prize'),
            IO('/Game/InteractiveObjects/Doors/Atlas/_Design/IO_Door_130x250_Atlas_ShelfDoor'),
            IO('/Game/InteractiveObjects/Doors/Atlas/_Design/IO_Door_400x400_SlideLeftAndRight_AtlasHQ_Generic'),
            IO('/Game/InteractiveObjects/Doors/Atlas/_Design/IO_Door_AtlasHQ_Elevator_Exterior'),
            IO('/Game/InteractiveObjects/Doors/Atlas/_Design/IO_Door_AtlasHQ_Elevator_Interior_Short'),
            IO('/Game/InteractiveObjects/Doors/Atlas/_Design/IO_Door_AtlasHQ_Elevator_Interior_Tall'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Doors/City/_Design/IO_Door_1630x600_MeltHole_GiantDoor'),
            IO('/Game/InteractiveObjects/Doors/City/_Design/IO_Door_1630x600_SlideUp_GiantDoor'),
            IO('/Game/InteractiveObjects/Doors/CoV/_Design/IO_Door_CoV_SwingingGate_V1'),
            IO('/Game/InteractiveObjects/Doors/Default/1000x600/IO_Door_1000x600_SlideLeftAndRight'),
            IO('/Game/InteractiveObjects/Doors/Default/800x600/IO_Door_800x600_SlideUp'),
            IO('/Game/InteractiveObjects/Doors/Eden_6/_Design/IO_Door_130x250_Rotate_Watership'),
            IO('/Game/InteractiveObjects/Doors/Eden_6/_Design/IO_Door_400x400_SlideLeftAndRight_Eden6_Generic_IronBear'),
            IO('/Game/InteractiveObjects/Doors/Eden_6/_Design/IO_Door_Custom_Watership_RotateUp'),
            IO('/Game/InteractiveObjects/Doors/Eden_6/_Design/IO_Door_Marshfields_Custom_HiddenSpyDoor'),
            IO('/Game/InteractiveObjects/Doors/Eden_6/_Design/IO_Door_Watership_Custom_LabDoor'),
            IO('/Game/InteractiveObjects/Doors/Eridian/_Design/IO_Door_1000x600_SlideLeftAndRight_Eridian_Generic'),
            IO('/Game/InteractiveObjects/Doors/Eridian/_Design/IO_Door_400x400_SlideUp_Eridian_Generic'),
            IO('/Game/InteractiveObjects/Doors/Eridian/_Design/IO_Door_Large_SlideUp_Eridian_Generic1'),
            IO('/Game/InteractiveObjects/Doors/Global/_Design/IO_Door_ScalableForcefield'),
            IO('/Game/InteractiveObjects/Doors/Industrial/_Design/IO_Door_1000x600_SlideUp_Industrial_Generic'),
            IO('/Game/InteractiveObjects/Doors/Industrial/_Design/IO_Door_400x400_SlideUp_Industrial_Generic'),
            IO('/Game/InteractiveObjects/Doors/Maliwan/_Design/IO_Door_Custom_Rotate_2Piece_Maliwan'),
            # No timing parameters for these two
            #IO('/Game/InteractiveObjects/Doors/Maliwan/_Design/IO_Door_Maliwan_Shield_Large'),
            #IO('/Game/InteractiveObjects/Doors/Maliwan/_Design/IO_Door_Maliwan_Shield'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_130x250_Rotate_Mansion_NoFrame'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_130x250_Rotate_Mansion'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_400x400_2Piece_Atrium_IronBearDoor'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_400x400_Rotate_2Piece_BustOpenMansionDoor'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_400x400_Rotate_2Piece_Generic_IronBearDoor'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_CustomSize_Rotate_2Piece_IronGate'),
            IO('/Game/InteractiveObjects/Doors/Mansion/_Design/IO_Door_Mansion_Bookcase_500x500_SlideRight'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Doors/Mine/_Design/IO_Door_400x400_SlideUp_MinerDetails_DestroyableDoor'),
            IO('/Game/InteractiveObjects/Doors/Monastery/_Design/IO_Door_130x250_SlideDown_Monastery'),
            IO('/Game/InteractiveObjects/Doors/Monastery/_Design/IO_Door_400x400_LeftAndRight_Monastery_1'),
            IO('/Game/InteractiveObjects/Doors/Monastery/_Design/IO_Door_400x400_LeftAndRight_Monastery_SpecialTitleCard'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Doors/Monastery/_Design/IO_Door_400x400_SlideUp_Monastery_TombDoor'),
            IO('/Game/InteractiveObjects/Doors/Monastery/_Design/IO_Door_800x600_SlideUp_Monastery_Courtyard'),
            IO('/Game/InteractiveObjects/Doors/Motorcade/_Design/IO_Door_130x250_Rotate_Motorcade_OrphanageDoor'),
            IO('/Game/InteractiveObjects/Doors/Motorcade/_Design/IO_Door_130x250_SlideUp_Motorcade_BanditHideoutDoor'),
            IO('/Game/InteractiveObjects/Doors/Motorcade/_Design/IO_Door_400x400_Motorcade_RotateUp'),
            IO('/Game/InteractiveObjects/Doors/Motorcade/_Design/IO_Door_800x600_Motorcade_Rotate'),
            IO('/Game/InteractiveObjects/Doors/Motorcade/_Design/IO_Door_800x600_SlideLeftAndRight_Motorcade_BarnDoor'),
            IO('/Game/InteractiveObjects/Doors/Motorcade/_Design/IO_Door_SkagFarm_400x400_RotateUp'),
            # Leave this one alone, doesn't ever impede movement.
            #IO('/Game/InteractiveObjects/Doors/Nekro/_Design/IO_Door_Custom_CloakedRock'),
            # No timing parameters for these two
            #IO('/Game/InteractiveObjects/Doors/Nekro/_Design/IO_Door_Custom_Nekro_Crypt_Small'),
            #IO('/Game/InteractiveObjects/Doors/Nekro/_Design/IO_Door_Custom_Nekro_Crypt'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_1000x600_SlideLeftAndRight_Pandora'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_1000x600_SlideUp_Pandora_Generic'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_130x250_Lynchwood_SlideLeft1'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_1630x1200_SlideUp_SecretGarageDoor'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_400x400_SlideUp_Pandora_Generic'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_CustomSize_Rotate_2Piece_CovRecruitmentDoor_Small'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_CustomSize_Rotate_2Piece_CovRecruitmentDoor'),
            # Only main TimelineLength found; skip it for now...
            #IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_CustomSize_Rotate_2Piece_MagnetDoor'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_CustomSize_RotateUp_Pandora_TunnelCap'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_CustomSize_SlideUp_Pandora_CarHook'),
            IO('/Game/InteractiveObjects/Doors/Pandora/_Design/IO_Door_Pandora_130x250_Rotate'),
            IO('/Game/InteractiveObjects/Doors/Prison/_Design/IO_Door_130x250_SlideUp_PrisonBars'),
            IO('/Game/InteractiveObjects/Doors/Prison/_Design/IO_Door_130x250_SlideUp_PrisonMetal'),
            IO('/Game/InteractiveObjects/Doors/Prison/_Design/IO_Door_400x400_SlideUpAndDown_Prison'),
            IO('/Game/InteractiveObjects/Doors/Prison/_Design/IO_Door_400x400_SlideUp_Prison'),
            IO('/Game/InteractiveObjects/Doors/Promethea/_Design/IO_Door_1000x600_SlideUp_Promethea_Generic'),
            # No timing parameters -- calls out to Door_Eden6_VehicleSpawner's AS_VehicleDoor_Open and handled above, though.
            #IO('/Game/InteractiveObjects/Doors/Promethea/_Design/IO_Door_1000x600_SlideUp_Promethea_Vehicle2'),
            IO('/Game/InteractiveObjects/Doors/Promethea/_Design/IO_Door_400x400_SlideUp_Promethea_Generic'),
            IO('/Game/InteractiveObjects/Doors/SpaceShips/_Design/IO_Door_130x250__SlideUp_Spaceships_Generic'),
            IO('/Game/InteractiveObjects/Doors/SpaceShips/_Design/IO_Door_400x400_SlideDown_Spaceships_Generic'),
            IO('/Game/InteractiveObjects/Doors/SpaceShips/_Design/IO_Door_400x400_SlideRight_Spaceships_Generi'),
            IO('/Game/InteractiveObjects/Doors/SpaceShips/_Design/IO_Door_400x400_SlideUp_Spaceships_Generic'),
            IO('/Game/PatchDLC/BloodyHarvest/InteractiveObjects/Doors/_Design/IO_Door_BloodyHarvest_Rotate_2Piece_IronGate'),
            # No timing parameters for these two
            #IO('/Game/PatchDLC/Event2/InteractiveObjects/Doors/_Design/IO_Door_400x400_Rotate_2Piece_Generic_IronBearDoor_Cartels'),
            #IO('/Game/PatchDLC/Event2/InteractiveObjects/Doors/_Design/IO_Door_CustomSize_Rotate_2Piece_IronGate_CartelsVar'),
            IO('/Game/PatchDLC/Ixora/InteractiveObjects/Doors/IO_Door_130x250_SlideUp_Motorcade_BanditHideoutDoor_GearUp'),
            # No timing parameters
            #IO('/Game/PatchDLC/Ixora/InteractiveObjects/Doors/IO_Door_400x400_SlideUp_Industrial_Generic_GearUp'),
            IO('/Geranium/InteractiveObjects/Doors/Facility/_Design/IO_Door_130x250_SlideUp_FacilityPlayerDoor1'),
            IO('/Geranium/InteractiveObjects/Doors/Facility/_Design/IO_Door_400x400_SlideLeftAndRight_FacilityIBDoor2'),
            IO('/Geranium/InteractiveObjects/Doors/Facility/_Design/IO_Door_400x400_SlideUp_FacilityIBDoor1'),
            IO('/Geranium/InteractiveObjects/Doors/Facility/_Design/IO_Door_800x600_SlideUpAndDown_FacilitySmallVehicleDoor2'),
            IO('/Geranium/InteractiveObjects/Doors/Facility/_Design/IO_Door_800x600_SlideUp_FacilitySmallVehicleDoor'),
            IO('/Geranium/InteractiveObjects/Doors/Facility/_Design/IO_Door_800x800_Rotate_IBArenaDoor'),
            # No timing parameters
            #IO('/Geranium/InteractiveObjects/Doors/Forest/_Design/IO_Door_Forest_TrainCrash'),
            IO('/Geranium/InteractiveObjects/Doors/Frontier/_Design/IO_Door_130x250_SlideUp_FrontierPlayerDoor'),
            IO('/Geranium/InteractiveObjects/Doors/Frontier/_Design/IO_Door_400x400_SlideLeftAndRight_FrontierIBDoor'),
            IO('/Geranium/InteractiveObjects/Doors/Frontier/_Design/IO_Door_400x400_VaultDoor'),
            IO('/Geranium/InteractiveObjects/Doors/IO_Door_130x250_SaloonDoor'),
            IO('/Geranium/InteractiveObjects/Doors/Lodge/_Design/IO_Door_400x400_Rotate_2Piece_Lodge_IronBear'),
            IO('/Geranium/InteractiveObjects/Doors/Lodge/_Design/IO_Door_Lodge_TreasureRoom'),
            IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/Factory/IO_Hib_Door_800x600_Factory'),
            # No timing parameters for these two
            #IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/MansionReskin/IO_Hib_Door2_400x400'),
            #IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/MansionReskin/IO_Hib_Door_400x400'),
            # This one can't be serialized currently, for some reason.
            #IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/MansionReskin/IO_Hib_Door_Bookcase'),
            # No timing parameters
            #IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/MansionReskin/IO_Hib_DoorFrame_130x250'),
            IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/Venue/IO_Hib_Door_Venue_BossGate'),
            # No timing parameters
            #IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/Village/IO_Hib_Door_130x250_Village'),
            IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/Village/IO_Hib_Door_IronGate'),
            IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/Woods/IO_Hib_Door_400x400_SlideDoor'),
            IO('/Hibiscus/InteractiveObjects/Systems/Doors/_Design/Woods/IO_Hib_Door_800x600_SlideDoor'),
            IO('/Ixora2/InteractiveObjects/Doors/IO_Door_400x400_SlideUp_Eridian_Generic'),
            # No timing parameters
            #IO('/Ixora2/InteractiveObjects/Doors/IO_Door_Custom_Eridian'),
            IO('/Ixora2/InteractiveObjects/Doors/IO_Door_SlideLeftAndRight_AlleyGate'),
            ]),
        ('Switches', global_scale, [
            # find $(find . -name Switches) -name "IO_*.uasset" | sort -i | cut -d. -f2
            IO('/Game/InteractiveObjects/Switches/Circuit_Breaker/_Design/IO_Switch_Circuit_Breaker_V1'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Switches/ControlPanel_Crane/_Design/IO_Switch_ControlPanel_Crane'),
            IO('/Game/InteractiveObjects/Switches/CoV/IO_Switch_CoV_SkullSwitch_V1'),
            IO('/Game/InteractiveObjects/Switches/CoV/Kitbash/_Design/IO_Switch_CoV_Kitbash_V1'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Switches/CoV/Target/IO_SwitchDamagable_CoV_TargetCeiling_V1'),
            IO('/Game/InteractiveObjects/Switches/CoV/Target/IO_SwitchDamagable_CoV_Target_V2'),
            IO('/Game/InteractiveObjects/Switches/Detonator/_Design/IO_Switch_Detonator_V1'),
            IO('/Game/InteractiveObjects/Switches/Eridian/_Design/IO_Switch_EridianSwitch_V1'),
            IO('/Game/InteractiveObjects/Switches/Industrial/Button/_Design/IO_Switch_GenericButton_V1'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Switches/Industrial/Keyboard/_Design/IO_Switch_Industrial_Keyboard_V1'),
            IO('/Game/InteractiveObjects/Switches/Lever/Design/IO_Switch_Industrial_FloorLever_V1'),
            IO('/Game/InteractiveObjects/Switches/Lever/Design/IO_Switch_Industrial_Prison'),
            IO('/Game/InteractiveObjects/Switches/Promethea/_Design/IO_Switch_Promethea_Generic_V1'),
            # No timing parameters
            #IO('/Game/InteractiveObjects/Switches/_Shared/_Design/IO_ChangeOfHeart_DoorbellButton'),
            IO('/Game/InteractiveObjects/Switches/Switch/Design/IO_Switch_IndustrialSwitch_V1'),
            IO('/Game/InteractiveObjects/Switches/WheelValve/Design/IO_Switch_Industrial_WheelValve_V1'),
            IO('/Game/PatchDLC/BloodyHarvest/InteractiveObjects/Switches/_Design/IO_Switch_SkullSwitch',
                level='BloodyHarvest_P',
                ),
            IO('/Game/InteractiveObjects/MissionUsable/_Design/MansionInvestigationObjects/IO_Switch_StatueButton',
                label="Hidden Statue Button in Jakobs Estate",
                level='Mansion_P',
                ),
            ]),
        ('More Containers', global_scale, [
            # This basically just speeds up the turn-to-green which allows it to be opened
            IO('/Game/Lootables/_Design/Classes/Eridian/BPIO_Lootable_Eridian_WhiteChestCrystal'),
            ]),
        ('Other Objects', global_scale, [
            # Needs some other tweaks as well, done below.
            IO('/Game/InteractiveObjects/SlotMachine/_Shared/_Design/BPIO_SlotMachine'),
            IO('/Game/InteractiveObjects/MissionScripted/_Design/IO_MissionScripted_StatueManufacturingMachine',
                label='Golden Calves Statue Scanner/Printer',
                level='Sacrifice_P',
                ),
            IO('/Game/InteractiveObjects/MissionUsable/_Design/IO_MissionUsable_SlidingDesk_Lamp',
                label="Rhys's Sliding Desk (Lamp)",
                level='AtlasHQ_P',
                ),
            IO('/Game/InteractiveObjects/MissionScripted/_Design/IO_MissionScripted_SlidingDesk',
                label="Rhys's Sliding Desk (Desk)",
                level='AtlasHQ_P',
                ),
            IO('/Game/InteractiveObjects/MissionUsable/_Design/MansionInvestigationObjects/IO_MissionUsable_ExplodingStatue',
                label="Exploding Busts in Jakobs Estate",
                level='Mansion_P',
                ),
            IO('/Game/InteractiveObjects/MissionUsable/_Design/MansionInvestigationObjects/IO_MissionUsable_SlidingPictureFrame',
                label="Sliding Pictures in Jakobs Estate",
                level='Mansion_P',
                ),
            IO('/Game/InteractiveObjects/MissionUsable/_Design/MansionInvestigationObjects/IO_MissionUsable_SpinningBookShelf',
                label="Rotating Bookshelves in Jakobs Estate",
                level='Mansion_P',
                ),
            IO('/Game/InteractiveObjects/MissionSpecificObjects/GrandTour/_Design/BP_IO_StageProp_UpDown',
                label="Stage Props in Jakobs Estate",
                level='Mansion_P',
                ),
            IO('/Game/InteractiveObjects/MissionUsable/_Design/IO_MissionUsable_AureliasSkeletons_MovableBed',
                label="Sliding Bed in 'Sacked' mission",
                level='Mansion_P',
                ),
            ]),
        ]:

    mod.header(category)

    for io_obj in io_objs:

        if verbose:
            print('Processing {}'.format(io_obj.path))

        if io_obj.scale is None:
            io_obj.scale = cat_scale

        mod.comment(io_obj.label)
        obj = data.get_data(io_obj.path)
        if not obj:
            print('WARNING - Could not be serialized: {}'.format(io_obj.path))
            continue

        if not checked_ver:
            if '_apoc_data_ver' not in obj[0] or obj[0]['_apoc_data_ver'] < min_apoc_jwp_version:
                raise RuntimeError('In order to generate a valid mod, you MUST use Apocalyptech\'s JWP fork which serializes to version {}'.format(min_apoc_jwp_version))
            checked_ver = True

        found_primary = False
        did_main = False
        did_curve = False
        for export in obj:
            if export['_jwp_object_name'] == io_obj.last_bit_c:
                found_primary = True
                if 'Timelines' in export:
                    for timeline_idx, timeline_ref in enumerate(export['Timelines']):
                        timeline_exp = timeline_ref['export']
                        if verbose:
                            print(' - Processing timeline {} (export {})'.format(timeline_idx, timeline_exp))
                        if timeline_exp != 0:
                            timeline = obj[timeline_exp-1]

                            # This one's not actually required (and doesn't seem to do anything), but I feel weird *not* specifying it.
                            if 'TimelineLength' in timeline and timeline['TimelineLength'] != 0:
                                did_main = True
                                mod.reg_hotfix(Mod.LEVEL, io_obj.level,
                                        io_obj.full_path,
                                        f'Timelines.Timelines[{timeline_idx}].Object..TimelineLength',
                                        round(timeline['TimelineLength']/io_obj.scale, 6))

                            # Now process all our various curves
                            for trackname, curve_var in [
                                    ('EventTracks', 'CurveKeys'),
                                    ('FloatTracks', 'CurveFloat'),
                                    # I think VectorTracks is generally not needed; more used for
                                    # rotation+position info, perhaps?
                                    ('VectorTracks', 'CurveVector'),
                                    ]:
                                if trackname in timeline:
                                    if verbose:
                                        print('   - Processing {}'.format(trackname))
                                    for track_idx, track_ref in enumerate(timeline[trackname]):
                                        track_exp = track_ref[curve_var]['export']
                                        if verbose:
                                            print('     - On curve {} (export {})'.format(track_idx, track_exp))
                                        if track_exp != 0:
                                            curve = obj[track_exp-1]
                                            for inner_curve_var in ['FloatCurve', 'FloatCurves']:
                                                if inner_curve_var in curve:
                                                    for key_idx, key in enumerate(curve[inner_curve_var]['Keys']):
                                                        if key['time'] != 0:
                                                            did_curve = True
                                                            mod.reg_hotfix(Mod.LEVEL, io_obj.level,
                                                                    io_obj.full_path,
                                                                    f'Timelines.Timelines[{timeline_idx}].Object..{trackname}.{trackname}[{track_idx}].{curve_var}.Object..{inner_curve_var}.Keys.Keys[{key_idx}].Time',
                                                                    round(key['time']/io_obj.scale, 6))


        if not found_primary:
            raise RuntimeError('Could not find main export for {}'.format(io_obj.path))

        if not did_main and not did_curve:
            print('NOTICE - No timing parameters found for {}'.format(io_obj.path))
            mod.comment('(no timing parameters found to alter)')
        elif not did_main:
            # This honestly hardly matters; it doesn't look like this attr's really used
            # for much, anyway.
            print('NOTICE - No main TimelineLength found for {}'.format(io_obj.path))
        elif not did_curve:
            print('NOTICE - No curve timings found for {}'.format(io_obj.path))

        mod.newline()

# TODO: DLC1
mod.header('Slot Machine Tweaks')
mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/InteractiveObjects/SlotMachine/_Shared/_Design/BPIO_SlotMachine',
        'ExecuteUbergraph_BPIO_SlotMachine',
        1513,
        5,
        5/global_scale)
mod.bytecode_hotfix(Mod.LEVEL, 'MatchAll',
        '/Game/InteractiveObjects/SlotMachine/_Shared/_Design/BPIO_SlotMachine',
        'ExecuteUbergraph_BPIO_SlotMachine',
        2889,
        1,
        1/global_scale)
mod.newline()

# Exploding Statues (in Jakobs Estate)
mod.header('Exploding Statue Tweaks')
for obj_name in [
        'Mansion_M_AureliasSkeletons.Mansion_M_AureliasSkeletons:PersistentLevel.IO_MissionUsable_ButtonStatue_2',
        'Mansion_M_EP09GrandTour.Mansion_M_EP09GrandTour:PersistentLevel.IO_MissionUsable_ExplodingStatue_3',
        'Mansion_M_EP09GrandTour.Mansion_M_EP09GrandTour:PersistentLevel.IO_MissionUsable_ExplodingStatue_1758',
        'Mansion_M_EP09GrandTour.Mansion_M_EP09GrandTour:PersistentLevel.IO_MissionUsable_ExplodingStatue_1388',
        'Mansion_P:PersistentLevel.IO_MissionUsable_ExplodingStatue_3',
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'/Game/Maps/Zone_2/Mansion/{obj_name}.RotateStatue',
            'TheTimeline.Length',
            1/global_scale,
            )
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'/Game/Maps/Zone_2/Mansion/{obj_name}.BP_IO_LootSpawnComponent',
            'DelayBeforeSpawningLoot',
            1/global_scale,
            )
mod.newline()

# Sliding Paintings (in Jakobs Estate)
mod.header('Sliding Painting Tweaks')
for obj_name in [
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_10',
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_11',
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_5',
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_6',
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_7',
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_8',
        'Mansion_Library.Mansion_Library:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_9',
        'Mansion_Theater.Mansion_Theater:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_5',
        'Mansion_Theater.Mansion_Theater:PersistentLevel.IO_MissionUsable_SlidingPictureFrame_8',
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'/Game/Maps/Zone_2/Mansion/{obj_name}.MoveFrame',
            'TheTimeline.Length',
            1/global_scale,
            )
mod.newline()

# Jakobs Estate Stage Props
mod.header('Jakobs Estate Stage Prop Tweaks')
mansion_base = '/Game/Maps/Zone_2/Mansion/Mansion_M_EP09GrandTour.Mansion_M_EP09GrandTour:PersistentLevel'
for obj_name, delay in [
        ('IO_Switch_IndustrialSwitch_V_1142', 1.2),
        ('IO_Switch_IndustrialSwitch_V_2148', 1.2),
        ('IO_Switch_IndustrialSwitch_V_991', 2.2),
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'{mansion_base}.{obj_name}',
            'EndSwitchMovementDelay',
            round(delay/global_scale, 6),
            )
for obj_name, duration in [
        ('E11GrandTour_BackgroundProp', 2.5),
        ('E11GrandTour_LeftProp', 1.5),
        ('E11GrandTour_RightProp', 1.5),
        ]:
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'{mansion_base}.{obj_name}',
            'DurationOfPropMovement',
            round(duration/global_scale, 6),
            )
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'{mansion_base}.{obj_name}.Timeline_0',
            'TheTimeline.Length',
            round(1/global_scale, 6),
            )
    mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
            f'{mansion_base}.{obj_name}.Timeline_0',
            'TheTimeline.Events.Events[0].Time',
            round(0.5/global_scale, 6),
            )
mod.newline()

# Spinning Bookshelves
mod.header('Jakobs Estate Spinning Bookshelf Tweaks')
mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
        '/Game/Maps/Zone_2/Mansion/Mansion_P.Mansion_P:PersistentLevel.EasterEgg_SpiningBookshelf',
        'LootSpawnDelay',
        5/global_scale)
mod.newline()

# Sliding Bed in Sacked
mod.header('Sliding Bed in Sacked')
mod.reg_hotfix(Mod.LEVEL, 'Mansion_P',
        '/Game/Maps/Zone_2/Mansion/Mansion_M_AureliasSkeletons.Mansion_M_AureliasSkeletons:PersistentLevel.IO_MissionUsable_AureliasSkeletons_MovableBed_2.Move Bed',
        'TheTimeline.Length',
        2/global_scale)
mod.newline()

# `getall Elevator`
mod.header('Elevators')
for label, level, obj_name, speed, travel_time in sorted([
        ('The Droughts - Taking Flight (Sanctuary III Drydock)', 'Prologue_P',
            '/Game/Maps/Zone_0/Prologue/Prologue_M_Ep04_EarnSpaceship.Prologue_M_Ep04_EarnSpaceship:PersistentLevel.Elevator_Ep04_Prologue',
            175, 10),
        ('Meridian Outskirts - Under Rax/Max Platform', 'Outskirts_P',
            '/Game/Maps/Zone_1/Outskirts/Outskirts_LowerSector.Outskirts_LowerSector:PersistentLevel.Elevator_UnderBridge_2',
            120, 10),
        ('Meridian Outskirts - Main upper/lower Elevator', 'Outskirts_P',
            '/Game/Maps/Zone_1/Outskirts/Outskirts_Mission.Outskirts_Mission:PersistentLevel.Elevator_Outskirts_Refugee',
            400, 10),
        ('Skywell-27 - Main Elevator', 'OrbitalPlatform_P',
            '/Game/Maps/Zone_1/OrbitalPlatform/OrbitalPlatform_Combat.OrbitalPlatform_Combat:PersistentLevel.Elevator_Cargo_OrbitalPlatform_2',
            2000, 10),
        # This one still feels a bit slow to me; I think it might not fully use these values?
        # But whatever, it's not slow enough for me to care enough to look into more.
        ('Skywell-27 - Boss Elevator', 'OrbitalPlatform_P',
            '/Game/Maps/Zone_1/OrbitalPlatform/OrbitalPlatform_Boss.OrbitalPlatform_Boss:PersistentLevel.Elevator_Cargo_OrbitalPlatform_2',
            200, 10),
        ('Atlas HQ - Main Office Elevator (initial trip up)', 'AtlasHQ_P',
            '/Game/Maps/Zone_1/AtlasHQ/AtlasHQ_M_EP06OfficeSpaceInvaders.AtlasHQ_M_EP06OfficeSpaceInvaders:PersistentLevel.Elevator_Ep06_AtlasHQ_V_2',
            250, 47),
        ('Atlas HQ - Smaller Elevator', 'AtlasHQ_P',
            '/Game/Maps/Zone_1/AtlasHQ/AtlasHQ_M_EP06OfficeSpaceInvaders.AtlasHQ_M_EP06OfficeSpaceInvaders:PersistentLevel.Elevator_Ep06_AtlasHQ_V_0',
            #250/2, 5*2),
            250, 5),
        ('Cistern of Slaughter', 'CreatureSlaughter_P',
            '/Game/Maps/Slaughters/CreatureSlaughter/CreatureSlaughter_P.CreatureSlaughter_P:PersistentLevel.Elevator_CreatureSlaughter',
            400, 10),
        ('Floodmoor Basin - Knotty Peak', 'Wetlands_P',
            '/Game/Maps/Zone_2/Wetlands/Wetlands_Dynamic.Wetlands_Dynamic:PersistentLevel.Elevator_WetlandsLodge_3326',
            400, 10),
        # May do alt scaling for this, and there's probably ubergraph stuff involved.  Check that out once we get there.
        #('Floodmoor Basin - Rocket Elevator', 'Wetlands_P',
        #    '/Game/Maps/Zone_2/Wetlands/Wetlands_M_DudeBro.Wetlands_M_DudeBro:PersistentLevel.Elevator_Rocket',
        #    900, 7),
        ('The Anvil - Sauce Room', 'Prison_P',
            '/Game/Maps/Zone_2/Prison/Prison_M_EP08PrisonBreak.Prison_M_EP08PrisonBreak:PersistentLevel.Elevator_PrisonArmory_1624',
            350, 10),
        ('Jakobs Estate', 'Mansion_P',
            '/Game/Maps/Zone_2/Mansion/Mansion_M_EP09GrandTour.Mansion_M_EP09GrandTour:PersistentLevel.Elevator_Ep09_Mansion_592',
            175, 20),
        ]):
    mod.comment(label)
    # Honestly not sure if we need both of these, but we *do* need EarlyLevel.  I'm pretty
    # sure that the one we *actually* need is TravelTime -- I think the Speed ends up
    # getting dynamically set.  Whatever, it doesn't *hurt*.
    mod.reg_hotfix(Mod.EARLYLEVEL, level,
            obj_name,
            'ElevatorSpeed',
            speed*global_scale,
            )
    mod.reg_hotfix(Mod.EARLYLEVEL, level,
            obj_name,
            'ElevatorTravelTime',
            travel_time/global_scale,
            )
    if 'Elevator_Ep06_AtlasHQ_V_0' in obj_name:
        # For some reason, at our default speedup, this elevator often kills the player once
        # it gets to the bottom.  Setting killDelay to 0 seems to take care of that (as does
        # 1?  the default is 6).  No idea what that parameter actually does, but it's weird.
        # The `bCrushPlayers` seemed a likely culprit as well, but that doesn't seem to be
        # involved.
        mod.reg_hotfix(Mod.EARLYLEVEL, level,
                obj_name,
                'killDelay',
                0,
                )
    mod.newline()

# Some elevators (okay, possibly just the ones in Atlas HQ) need some extra ubergraph love
# once the mission is done -- the tweak above only seems to apply on the very first trip up.
mod.header('Post-Mission Elevator Tweaks')

# This is what speeds up the elevator for us on subsequent rides
mod.comment('Atlas HQ - Main Office Elevator')
mod.bytecode_hotfix(Mod.LEVEL, 'AtlasHQ_P',
        '/Game/Maps/Zone_1/AtlasHQ/AtlasHQ_M_EP06OfficeSpaceInvaders',
        'ExecuteUbergraph_AtlasHQ_M_EP06OfficeSpaceInvaders',
        6427,
        25,
        25/global_scale)
mod.newline()

# Make Fast Travel + Teleport digistruct animations disappear
# (note that the death respawn is totally separate from this, and handled via
# some AnimSequence tweaks above)
mod.header('Fast Travel / Teleport Animation Disable')

# A bunch of silliness in here, when I was looking at bundling this separately
# as its own mod and was considering multiple versions.  In the end, this just
# hardcodes an effective disabling of the whole sequence, and I could omit
# various bits of math.  But whatever, the work is done -- leaving it as-is.
default_duration = 6.5
default_unlock = 5.5
default_teleport = 1.5
unlock_scale = default_unlock/default_duration
teleport_scale = default_teleport/default_duration

# 0.5 - Effectively disables it
# 2 - Quite short, but still gets a tiny bit of the tunnel
new_duration = 0.5

min_timers = min(default_teleport, new_duration)

mod.reg_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Travel/Action_TeleportEffects.Default__Action_TeleportEffects_C',
        'Duration',
        new_duration,
        )

# Adjust delay on unlocking resources (whatever that means; haven't figured out
# what's not available when "locked")
mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Travel/Action_TeleportEffects',
        'ExecuteUbergraph_Action_TeleportEffects',
        1119,
        default_unlock,
        max(min_timers, round(new_duration*unlock_scale, 6)),
        )

# Adjust delay on actually teleporting
mod.bytecode_hotfix(Mod.PATCH, '',
        '/Game/PlayerCharacters/_Shared/_Design/Travel/Action_TeleportEffects',
        'ExecuteUbergraph_Action_TeleportEffects',
        391,
        default_teleport,
        max(min_timers, round(new_duration*teleport_scale, 6)),
        )

mod.newline()

# Golden Calves Statue Scanner
mod.header('Custom Golden Calves Statue Scanner Tweaks')

mod.comment('Shorten scanner-light animation')
mod.reg_hotfix(Mod.LEVEL, 'Sacrifice_P',
        '/Game/InteractiveObjects/MissionScripted/Effects/System/PS_Scanning_Machine',
        'Emitters.Emitters[0].Object..LODLevels.LODLevels[0].Object..RequiredModule.Object..EmitterDuration',
        12/global_scale)
mod.reg_hotfix(Mod.LEVEL, 'Sacrifice_P',
        '/Game/InteractiveObjects/MissionScripted/Effects/System/PS_Scanning_Machine',
        'Emitters.Emitters[0].Object..LODLevels.LODLevels[0].Object..Modules.Modules[1].Object..Lifetime.Distribution.Object..Constant',
        12/global_scale)
mod.newline()

mod.comment('Shorten delay between scanning + printing')
mod.reg_hotfix(Mod.LEVEL, 'Sacrifice_P',
        '/Game/Maps/Zone_0/Sacrifice/Sacrifice_M_GoldenCalves.Sacrifice_M_GoldenCalves:PersistentLevel.IO_MissionScripted_StatueManufacturingMachine_2.Scanning',
        'TheTimeline.Length',
        12/global_scale)
mod.reg_hotfix(Mod.LEVEL, 'Sacrifice_P',
        '/Game/Maps/Zone_0/Sacrifice/Sacrifice_M_GoldenCalves.Sacrifice_M_GoldenCalves:PersistentLevel.IO_MissionScripted_StatueManufacturingMachine_2.Scanning',
        'TheTimeline.Events.Events[0].Time',
        round(4.014948/global_scale, 6))
mod.newline()

# Not sure what most of this does, though at least one of them is an initial delay when
# you stick the posters in, before they start getting sucked into the machine.
mod.comment('Tweak a few shorter delays')
for index, cur_val in [
        (575, 0.2),
        (899, 2.0),
        # Honestly not sure if these two should be combined; not sure what they control and it's
        # not super obvious.
        (976, 1.0),
        (2539, 1.0),
        ]:
    mod.bytecode_hotfix(Mod.LEVEL, 'Sacrifice_P',
            '/Game/InteractiveObjects/MissionScripted/_Design/IO_MissionScripted_StatueManufacturingMachine',
            'ExecuteUbergraph_IO_MissionScripted_StatueManufacturingMachine',
            index,
            cur_val,
            round(cur_val/global_scale, 6))
mod.newline()

# This is all pretty stupid.  The pouring animation is hardcoded to 20 seconds; we chop
# six seconds off to get it down to 14.  That's the minimum we can do without causing
# the game to skip dialogue.
pour_duration = 14
mod.header('Coffee-pouring Animations during Rise and Grind')
# This one handles the visual fill-level on the side
# getall IO_MissionPlaceable_RiseAndGrind_3Thermos_C FillDuration
mod.reg_hotfix(Mod.LEVEL, 'City_P',
        '/Game/Maps/Zone_1/City/City_M_RiseAndGrind.City_M_RiseAndGrind:PersistentLevel.RiseAndGrind_Thermos',
        'FillDuration',
        pour_duration)
# Next two handle the actual pouring animation
# getall DistributionFloatConstant Constant name=RequiredDistributionSpawnRate outer=PS_CoffeePour_Stream
mod.reg_hotfix(Mod.LEVEL, 'City_P',
        '/Game/Missions/Side/Zone_1/City/RiseAndGrind/Effects/Systems/PS_CoffeePour_Stream.PS_CoffeePour_Stream:ParticleModuleSpawn_1.RequiredDistributionSpawnRate',
        'Constant',
        pour_duration)
# getall ParticleModuleRequired EmitterDuration name=ParticleModuleRequired_1 outer=PS_CoffeePour_Stream
mod.reg_hotfix(Mod.LEVEL, 'City_P',
        '/Game/Missions/Side/Zone_1/City/RiseAndGrind/Effects/Systems/PS_CoffeePour_Stream.PS_CoffeePour_Stream:ParticleModuleRequired_1',
        'EmitterDuration',
        pour_duration)
# *This* is the timer which activates the pickup and allows the mission to continue
mod.bytecode_hotfix(Mod.LEVEL, 'City_P',
        '/Game/Maps/Zone_1/City/City_M_RiseAndGrind',
        'ExecuteUbergraph_City_M_RiseAndGrind',
        6616,
        20,
        pour_duration)
mod.newline()

# The remaining speed improvements here would have to be done in relation to a
# `BPChar_GenericMonk` named "Brother Catus" spawning in to run over and open the
# door.  We could make him faster, but the bulk of the time is actually spent in
# the spawning animation, so walking/sprinting speed tweaks really don't help
# him much.  And also, since he's not actually an individual BPChar of his own,
# tweaking him would also tweak all other monks in the area, which I'd rather not
# do.  Anyway, these two tweaks improve the opening time pretty well anyway, so
# I'm content with that.  (Another thing to do would be to try and cut Catus out
# of the loop entirely, but I just don't care enough to try and do that without
# breaking the mission entirely.)
mod.header('Speed up second Athenas Bell of Peace door opening')
mod.bytecode_hotfix(Mod.LEVEL, 'Monastery_P',
        '/Game/Missions/Plot/Mission_Ep06_MeetMaya',
        'ExecuteUbergraph_Mission_Ep06_MeetMaya',
        39968,
        3,
        0)
mod.bytecode_hotfix(Mod.LEVEL, 'Monastery_P',
        '/Game/Maps/Zone_1/Monastery/Monastery_Mission_Ep06_MeetMaya',
        'ExecuteUbergraph_Monastery_Mission_Ep06_MeetMaya',
        49863,
        1,
        0)
mod.newline()

# Don't let Ava spend so long shocked at Maya's death
mod.header("Speed up Ava's shock-at-Maya's-death time")
mod.reg_hotfix(Mod.LEVEL, 'CityBoss_P',
        '/Game/NonPlayerCharacters/Ava/_Design/Actions/Action_Ava_Loop_Grieve.Default__Action_Ava_Loop_Grieve_C',
        'LoopTime.Range.Value',
        15/global_scale)
mod.bytecode_hotfix(Mod.LEVEL, 'CityBoss_P',
        '/Game/Maps/Zone_1/CityBoss/CityBoss_Mission',
        'ExecuteUbergraph_CityBoss_Mission',
        31722,
        15,
        15/global_scale)
mod.newline()

# Peace Bells (or whatever) in Athenas.  Not actually doing this because the speed
# isn't too bad already, and the events they trigger actually happen immediately
# when you "use" them, anyway.  The Ubergraphs sometimes put in some artificial
# delays to make it seem like stuff's happening after, like with the door opening
# I tweaked, above, but it's not actually tied in with this.
if False:

    # Up in the main IO/BPIO section, this speeds up the striker itself...
    #('Large Bells in Athenas', 'Monastery_P', '/Game/InteractiveObjects/BonshuBell/Global/IO_MissionUsable_BonshuBell'),

    # ... and this next bit makes the bell ringing trigger at the right time
    mod.header('Large Bells on Athenas')
    bell_scale=5
    for obj_name in [
            '/Game/Maps/Zone_1/Monastery/Monastery_Mission_MonkMission.Monastery_Mission_MonkMission:PersistentLevel.IO_MissionUsable_BonshuBell_1',
            '/Game/Maps/Zone_1/Monastery/Monastery_Mission_Ep06_MeetMaya.Monastery_Mission_Ep06_MeetMaya:PersistentLevel.IO_MissionUsable_BonshuBell_0',
            '/Game/Maps/Zone_1/Monastery/Monastery_Mission_Ep06_MeetMaya.Monastery_Mission_Ep06_MeetMaya:PersistentLevel.IO_MissionUsable_BonshuBell_1',
            '/Game/Maps/Zone_1/Monastery/Monastery_Mission_Ep06_MeetMaya.Monastery_Mission_Ep06_MeetMaya:PersistentLevel.IO_MissionUsable_BonshuBell_4227',
            ]:
        for subobj in [
                'BellRinging',
                'StrikeBell',
                ]:
            full_obj = f'{obj_name}.{subobj}'
            mod.reg_hotfix(Mod.LEVEL, 'Monastery_P',
                    full_obj,
                    'TheTimeline.Length',
                    4/bell_scale,
                    )
            if subobj == 'StrikeBell':
                mod.reg_hotfix(Mod.LEVEL, 'Monastery_P',
                        full_obj,
                        'TheTimeline.Events.Events[0].Time',
                        1/bell_scale,
                        )
        #mod.reg_hotfix(Mod.LEVEL, 'Monastery_P',
        #        obj_name,
        #        'TheTimeline.PlayRate',
        #        bell_scale,
        #        )
    mod.newline()

# Honestly not sure yet if I want to put this in here, but I'm doing it for now...
# Can split it out later if I want.
mod.header('NPC Walking Speeds')

for charname, obj_name, scale in sorted([
        ('Claptrap',
            '/Game/NonPlayerCharacters/Claptrap/_Design/Character/BpChar_Claptrap',
            global_char_scale),
        ('Ellie',
            '/Game/NonPlayerCharacters/Ellie/_Design/Character/BPChar_Ellie',
            global_char_scale),
        ('Lilith',
            '/Game/NonPlayerCharacters/Lilith/_Design/Character/BPChar_Lilith',
            global_char_scale),
        ('Ace Baron (Healers and Dealers)',
            '/Game/NonPlayerCharacters/_Promethea/MedicalAssistant/_Design/Character/BPChar_MedicalAssistant',
            global_char_scale),
        # Vic's got a long way to run -- really bump this one up
        ('Vic (Head Case)',
            '/Game/NonPlayerCharacters/_Pandora/HeadCaseGirl/_Design/Character/BPChar_HeadCaseGirl',
            3),
        # Maya's mostly fine, but there's a couple of cases where it'd be nice if she were a bit faster
        ('Maya',
            '/Game/NonPlayerCharacters/Maya/_Design/Character/BPChar_Maya',
            global_char_scale),
        # Ava's honestly not too bad, but she's got a long run back from the graveyard
        ('Ava',
            '/Game/NonPlayerCharacters/Ava/_Design/Character/BPChar_Ava',
            global_char_scale),
        # This one's a bit silly 'cause he walks all of like three feet, but whatever.
        ('Liam (Atlas HQ Security Guard)',
            '/Game/NonPlayerCharacters/_Promethea/AtlasSoldier/_Design/Character/BPChar_AtlasSecurityGuard',
            global_char_scale),
        ('Glenn the Ratch',
            '/Game/NonPlayerCharacters/_Promethea/TalkingRatch/_Design/Character/BPChar_TalkingRatch',
            global_char_scale),
        ('Terry the Ratch',
            '/Game/NonPlayerCharacters/_Promethea/TalkingRatch/_Design/Character/BPChar_GoodRatch',
            global_char_scale),
        # Not sure if this is really necessary, but he *can* lag behind in The Anvil.
        ('Brick',
            '/Game/NonPlayerCharacters/Brick/_Design/Character/BPChar_Brick',
            global_char_scale),
        # Also not sure how necessary this is; at the moment this hardly improves anything; just her
        # saunter over to construct the bomb, in Anvil.
        ('Tina',
            '/Game/NonPlayerCharacters/TinyTina/_Design/Character/BPChar_TinyTina',
            global_char_scale),
        ]):

    last_bit = obj_name.split('/')[-1]
    default_name = 'Default__{}_C'.format(last_bit)
    full_obj_name = '{}.{}'.format(obj_name, default_name)

    found_main = False
    char_data = data.get_data(obj_name)
    speed_walk = None
    speed_sprint = None
    have_slowdown = False
    for export in char_data:
        if export['_jwp_object_name'].lower() == default_name.lower():
            found_main = True
            if 'OakCharacterMovement' in export:
                if export['OakCharacterMovement']['export'] != 0:
                    move_export = char_data[export['OakCharacterMovement']['export']-1]
                    if 'MaxWalkSpeed' in move_export:
                        speed_walk = move_export['MaxWalkSpeed']['BaseValue']
                    else:
                        # The default
                        speed_walk = 600
                    if 'MaxSprintSpeed' in move_export:
                        speed_sprint = move_export['MaxSprintSpeed']['BaseValue']
                    else:
                        # The default
                        speed_sprint = 900
                    if 'NavSlowdownOptions' in move_export and 'SlowdownSpeed' in move_export['NavSlowdownOptions']:
                        have_slowdown = True
                else:
                    raise RuntimeError('Could not find OakCharacterMovement export in {}'.format(obj_name))
            else:
                raise RuntimeError('Could not find OakCharacterMovement in {}'.format(obj_name))
            break
    if not found_main:
        raise RuntimeError('Could not find {} in {}'.format(default_name, obj_name))

    mod.comment(charname)
    mod.reg_hotfix(Mod.CHAR, last_bit,
            full_obj_name,
            'OakCharacterMovement.Object..MaxWalkSpeed',
            '(Value={},BaseValue={})'.format(
                speed_walk*scale,
                speed_walk*scale,
                ),
            )
    mod.reg_hotfix(Mod.CHAR, last_bit,
            full_obj_name,
            'OakCharacterMovement.Object..MaxSprintSpeed',
            '(Value={},BaseValue={})'.format(
                speed_sprint*scale,
                speed_sprint*scale,
                ),
            )
    if have_slowdown:
        mod.reg_hotfix(Mod.CHAR, last_bit,
                full_obj_name,
                'OakCharacterMovement.Object..NavSlowdownOptions.bSlowdownNearGoal',
                'False',
                )
        mod.reg_hotfix(Mod.CHAR, last_bit,
                full_obj_name,
                'OakCharacterMovement.Object..NavSlowdownOptions.SlowdownSpeed.Value',
                1,
                )
    mod.newline()

# Some attempts to make loot-spewing pickups (bone piles, trash cans, etc) pick up more quickly.
# No luck yet!
if False:

    # The default for this attr (found in droppedinventoryitempickup objects) is 1.  I suspect this
    # *might* be something we could go for?  It feels like these items start auto-picking-up after
    # about 1sec.  I assume that the var means something like "if the item hasn't had a collision after
    # this many seconds, stop applying physics" or somesuch, at which point they're pick-upable.
    # I could be wrong about that, though.  At any rate, this statement looks okay to me but it never
    # seems to change the reported `getall` values.  Could be this is dynamically assigned or something.
    for hftype in [Mod.LEVEL, Mod.EARLYLEVEL]:
        for notify in [True, False]:
            mod.reg_hotfix(hftype, 'MatchAll',
                    '/Game/Pickups/_Shared/_Design/BP_OakConsumableItemPickup.Default__BP_OakConsumableItemPickup_C',
                    'NextImpactTimeThreshold',
                    0.1,
                    notify=notify)

    # So after some more experimentation, I think that the basic issue is that loot
    # doesn't get auto-picked-up until it's no longer being affected by physics.  The
    # engine just waits for them to get "settled" and *then* adds them into whatever
    # structure controls "these are the things you can auto-pick-up."  So in the end,
    # it's sot of the `ShouldAttachLoot` boolean which determines how quickly things
    # like ammo/health/money will get auto-picked up.  The `bSimulatePhysicsAfterOpening`
    # boolean is actually for the container itself, not the loot -- think of the way
    # cardboard boxes get physicsy after they've been opened.  I figured I'd try
    # turning that off too, anyway, just so any loot-attachment didn't get screwed
    # up.
    #
    # Anyway, first attempt: altering the Default__ object.  This just doesn't work;
    # the attrs never get updated on the map objects.  I think it's 'cause the map
    # objects are sort of hardcoded with the defaults already.
    for hf_type in [Mod.EARLYLEVEL, Mod.LEVEL]:
        for notify in [True, False]:
            mod.reg_hotfix(hf_type, 'Towers_P',
                    '/Game/Lootables/_Design/Classes/CoV/BPIO_Lootable_COV_CardboardBox.Default__BPIO_Lootable_COV_CardboardBox_C',
                    'bSimulatePhysicsAfterOpening',
                    'False',
                    notify=notify)
            mod.reg_hotfix(hf_type, 'Towers_P',
                    '/Game/Lootables/_Design/Classes/CoV/BPIO_Lootable_COV_CardboardBox.Default__BPIO_Lootable_COV_CardboardBox_C',
                    'ShouldAttachLoot',
                    'True',
                    notify=notify)

    # ... aaand testing this out by hitting each individual map object.  This *does*
    # work!  The cardboard boxes don't get physics after opening, the loot gets
    # "attached" inside, and money/health/ammo will get immediately auto-picked-up.
    # In the end I wouldn't be willing to do this, though, 'cause I kind of like
    # the default dispersal method (and it might end up weird for stuff like guns),
    # and also because I'd have to touch literally every single relevant object in
    # the game to do it this way.  Eesh.
    #
    # Anyway, the only other alternative here would be to see if there's *some* way
    # to tell the engine to auto-pick-up items even if they're being acted on by
    # physics.  It's possible that there's a boolean somewhere which'd do that (or
    # maybe some ubergraph stuff?) but I haven't found it yet, and don't really care
    # to work hard enough to find it.  I assume that that behavior isn't default
    # For A Reason -- like maybe it's very "expensive" in the engine to keep updating
    # those locations in realtime, in whatever structure controls auto-pick-up.
    # Anyway, for now I'm definitely giving up on it.
    for map_name in [
            '/Game/Maps/Zone_1/Towers/Towers_P',
            '/Game/Maps/Zone_1/Towers/Towers_Combat',
            '/Game/Maps/Zone_1/Towers/Towers_Light',
            ]:
        map_data = data.get_data(map_name)
        map_last = map_name.rsplit('/', 1)[-1]
        for export in map_data:
            if export['export_type'] == 'BPIO_Lootable_COV_CardboardBox_C':
                export_name = export['_jwp_object_name']
                obj_full = f'{map_name}.{map_last}:PersistentLevel.{export_name}'
                mod.reg_hotfix(Mod.EARLYLEVEL, 'Towers_P',
                        obj_full,
                        'bSimulatePhysicsAfterOpening',
                        'False',
                        notify=True)
                mod.reg_hotfix(Mod.EARLYLEVEL, 'Towers_P',
                        obj_full,
                        'ShouldAttachLoot',
                        'True',
                        notify=True)

mod.close()
