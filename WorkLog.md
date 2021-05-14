* added install instructions

## 2021-05-14 15:14:36.851582: clock-in

## 2021-05-13 17:37:43.499985: clock-out

* skipping hydra for hot reloading

* this works, but needs interval to refresh `gunicorn psidash.cli.main:server -b 0.0.0.0:8050 --reload --reload-extra-file psidash.yaml`
* allowed generation of server variable outside of main loop
* merging doesn't work with dot keywords. Example after merge:

```yaml
  dash.Dash:
    title: psidash basic
  jupyter_dash.JupyterDash:
    external_scripts: ${external_scripts}
    external_stylesheets: ${external_stylesheets}
    title: psidash
```

`dash.Dash` contents won't replace jupyter_dash.JupyterDash

## 2021-05-13 15:56:01.161331: clock-in

## 2021-05-12 18:29:35.791931: clock-out

* adding command line tool

## 2021-05-12 17:12:47.414452: clock-in

## 2021-05-11 17:15:33.523594: clock-out

* using new class dict syntax

## 2021-05-11 17:07:02.202455: clock-in

## 2021-05-11 16:55:49.763731: clock-out

* improved conf syntax, removed superfluous class keyword

## 2021-05-11 14:15:40.659822: clock-in

## 2021-05-07 18:36:04.714902: clock-out

* dot config tests

## 2021-05-07 17:52:33.644595: clock-in

## 2021-05-07 17:25:25.062441: clock-out

* adding dot config

## 2021-05-07 15:34:16.593435: clock-in

* moving conf up
## 2021-05-06 10:18:08.736571: clock-out

* moving conf into details
* moving callback demo to readme

## 2021-05-06 09:46:42.579395: clock-in

## 2021-05-06 00:46:45.402471: clock-out

* updating readme
* removing notebook in favor of markdown
* syncing markdown
* layout demo matching official plotly docs

## 2021-05-05 22:30:52.154170: clock-in

## 2021-05-05 15:06:45.258942: clock-out

* ignoring dev files
* cleaned up install

## 2021-05-05 13:00:16.563345: clock-in

## 2021-05-05 11:33:20.645548: clock-out

* storing callbacks in namedtuple, added bootstrap

## 2021-05-05 10:59:52.965222: clock-in

## 2021-05-05 10:57:22.433866: clock-out


## 2021-05-05 10:38:36.543471: clock-in

## 2021-05-04 18:01:51.122513: clock-out

* creating lambda signature

## 2021-05-04 17:01:37.235238: clock-in

## 2021-05-04 15:12:51.305971: clock-out

* added demo loading dash app from config
* running docker-compose from `report-generator/Docker/docker-compose.yaml`
* note: predscinc should generate a `docker-compose.yaml`

# 2021-05-04 13:36:55.133535: clock-in: T-10m 

