Code for an RPG Maker MZ Game

See my deviantart: https://www.deviantart.com/wfay42

# How Battle Events work

The battle event call tree is kind of complicated, so I try to spell it out here.

For example, for Nagas

* On the monster's Event
  * It sets `Naga Encounter Troop` equal to the `Troop` number for the encounter
  * Then it calls `Common Event: Naga Battle Lifecycle`
* `Common Event: Naga Battle Lifecycle`
  * Starts a `Battle Processing` to start a battle
  * After the battle ends, it checks if we won or escaped to decide if the Event
  on the map should be erased or not
  * Then it calls `Common-Event: Post-battle Reset`
* Within the `Troops` tab
  * The `Naga` and `Naga Queen` Troops have one `Battle Event`
  * It is set up with `Conditions: Turn End` and `Span: Turn`
  * The battle event calls `Common Event: Naga Battle`
* `Common Event: Naga Battle`
  * This calls `Common Event: Naga Battle <Character>` for each of the 3 characters
  * It then checks if all characters are affected by the full naga condition. If so,
  it flips a switch for `Common Event: Post-battle Reset` to use for Bad Ends,
  then aborts the fight.
* `Common Event: Naga Battle <Character Name>`
  * Each character has their own copy of this event
  * If character is affected by the base condition (`Naga`), we increment their `Naga Level`
  * Then we have a switch statement for each value of `Naga Level` to show the appropriate portrait
  * At the highest level, we change their state to include `Naga Confusion` meaning they
  have fully converted.
* `Common-Event: Post-battle Reset`
  * Shows any Bad Ends that happen based on set variables
  * Otherwise, resets all battle portraits and `<Character> Naga Level` variables,
  then recovers the whole party.
