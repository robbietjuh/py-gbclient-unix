# gbclient-unix

This is an implementation of a web based (label) printing system for Unix. In a nutshell, `gbclient-unix`:

* Waits for incoming API requests and then...
* serves a list of known printers on the local system...
* so that the client can put in a print job for a given HTML template...
* which is then converted into a PDF...
* and offered to CUPS to be printed.

## History

The original GBPrintServer was written as a small Windows utility, wrapping a simple HTTP API around Brother's label printing SDK. Brother does not seem to be offering Unix support for that SDK any time soon, though.
 
 So, seeing as we wanted to run GBPrintServer on a few Macs and Linux systems, it was time to write something ourselves.

## Installation

You can optionally set up a new virtualenv. All that's left is then to just install the required packages through pip.

```
virtualenv env/
pip install -r requirements.txt
```

You might want to set up additional settings in your `local_settings.py`.

## Usage

To start the server:

```
cd ~/path/to/git/repo
python gbclient
```

## API

`GET /api/v1/about`
Request details about the running server.

```
$ curl http://localhost:5000/api/v1/about
{
  "api_version": "2", 
  "hostname": "osx02.ad.local", 
  "platform": "Darwin", 
  "printers": [ ... ], 
  "version": "1.0"
}
```

`GET /api/v1/printer`
Request a list of printers.

```
$ curl http://localhost:5000/api/v1/printer
[
  {
    "id": "Brother_QL_560", 
    "location": "MacBook van R. de Vries", 
    "model": "Brother QL-560 CUPS", 
    "name": "Brother QL-560"
  }, 
  {
    "id": "Brother_MFC_J470DW", 
    "location": "MacBook van R. de Vries", 
    "model": "Brother MFC-J470DW CUPS", 
    "name": "Brother MFC-J470DW"
  }
]
```

`POST /api/v1/printer/<id>` Submit a new (label) print job

```
$ curl --data '{"label": "item", "item_id": "123", "storage_id": "456"}' \
→      -H "Content-Type: application/json" \
→      http://localhost:5000/api/v1/printer/Brother_QL_560
```

*Note:* This endpoint will just return 200 OK with an empty body.

*Note:* Your POST data must be a JSON string and must specify a `label`. This value will be used to determine the template to be used.

*Note:* Additional JSON key-value pairs will be passed along as context to the label template.

*Note:* You may want to change the location of your templates directory in `local_settings.py`.

## Templates

gbclient-unix uses Flask's template engine to generate HTML. It will then convert that HTML to a PDF and print it.

You can specify the location of your templates directory in `local_settings.py`. We've already added an example of a label in the `examples` directory.

All requests to print must include a `label` attribute. The value should exactly match the name of your template file, excluding the '.html' part.

## Media size

Please be aware of the `data-gbclient-media-size` attribute. You may add this attribute to the `<html>` tag of your label template. The value is then passed along to CUPS in order to determine the media size of your label. A valid value would be `Custom.62x25mm`, specifying a label of 62 by 25 millimeters.

If the `data-gbclient-media-size` attribute is not present on the first `<html>` tag, the default value `62mm` will be passed along to CUPS.

If you want to print through a regular printer, or want to print larger formats, you can also specify a media size like `A4` or `Letter`.

Use the following command to determine the officially supported media sizes for your printer of choice:

```
lpoptions -p <printer_id> -l
```

CUPS has excellent documentation on the allowed media sizes [here](https://www.cups.org/doc/options.html#OPTIONS). Really, you should check it out.

## Security

`gbclient-unix` does not provide any means of authentication at this point in time. It would be nice to have though, so if you feel like contributing some love I'd really appreciate that :-)