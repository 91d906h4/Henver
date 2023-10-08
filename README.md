# Henver HTTP Server

This is a simple Python HTTP Server. You can use it to host a static website or php pages (with restrictions).

## Usage

Use the following command to start the server.

```sh
python henver.py
```

## Config

- The config file is in `/config/main.ini`, you can adjust the settings in this file.
- All webpage and files should be deployed in folder `/public` (e.g. `index.html`, `favicon.ico`, etc.).
- You can place the error pages in `/public/error_pages`, or you can change the settings in `main.ini`.