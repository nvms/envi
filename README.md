### envi[ronment] spaces

```bash
git clone http://github.com/nvms/envi
cd envi
python setup.py install
envi
```

### dependencies

1. [An EWMH/NetWM compatible X Window Manager](https://en.wikipedia.org/wiki/Extended_Window_Manager_Hints).
2. `xwininfo`
3. `wmctrl`

### config

`~/.config/envi/config.yml`.

This sample config defines a 'music' and 'dev' space that each start a few applications. Arguments can be passed in brackets: `[args, ...]`. Using `;` as a delimiter, you can tell envi to do something immediately after opening the application. See the subl example below.

```yaml
music:
  pithos:
    height: 650
    width: 350
    x: 75
    y: 75
  rhythmbox:
    height: 650
    width: 1024
    x: 800
    y: 75
dev:
  subl[; notify-send "It's so sublime"; sh /some/script.sh]:
    height: 1567
    width: 1748
    x: 75
    y: 68
  firefox[--new-tab localhost:8000/ --devtools]:
    height: 1567
    width: 1994
    x: 1833
    y: 68
  nautilus:
    adjust: true
    height: 550
    width: 1251
    x: 1067
    y: 1630
  gnome-terminal:
    height: 477
    width: 1010
    x: 2817
    y: 1645
  gnome-terminal*:
    height: 477
    width: 1010
    x: 1817
    y: 1645
  gnome-terminal**:
    height: 477
    width: 1010
    x: 0
    y: 1645
```

### todo

In order of importance:

- [x] ~~Applications can have any number of arguments.~~
- [x] ~~Safely wait until an application has opened successfully: do we have a new WINID yet? If not, don't proceed. If yes, the application must have opened. This would remove the need for the global startup delay timer.~~
- [x] ~~Introduce capture command to dump details of focused window (x, y, w, h): `envi capture <float>`.~~
- [ ] Use `wmctrl` to switch between workspaces if a space is defined as being on anything other than the current one.
- [ ] More than one application with the same name. I might need to bootstrap the YAML loader.
   - [x] Workaround: In the config, place asterisks after the application name. The YAML loader doesn't count these as duplicates and therefore preserves them in the data it returns.
- [x] ~~Verbose output with `envi space {spacename} -v |--verbose`.~~
- [x] Look into output of `wmctrl -l [-p -x]`. Might be able to remove xdotool dependency entirely if this gives me everything I need. [Example and explaination](https://stackoverflow.com/questions/2250757/is-there-a-linux-command-to-determine-the-window-ids-associated-with-a-given-pro)

