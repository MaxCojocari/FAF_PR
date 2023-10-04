# LAB4

## Class Task

In this implementation we use localhost, so be sure that 8080 port is not occupied by the other process.

For running the server use `python3 in_class.py`.

Tasks done (see `in_class.py`):

- Created a webserver with 3 simple pages:
  - home `/`
  - contacts `/contacts`
  - about-us `/about-us`
- Created a template page for products that will incorporate products details:
  - product page `/products/x`, with `x = 0, 1, 2, ...`, see `handle_product_page_route` function for implementation details
- Created a product listing page:
  - products page `/products`, see `handle_products_route` for details
- If a requested page doesn't exist return a 404 error code;
  - Test `/products/x` with an index out of range, it will return 404 Not Found error

All contents of product listing pages and concrete product page are dynamiclly read from `data.json` file.
The Client sample which communicates with server developed in class thorugh TCP/IP can be found in `client.py`.

```shell
> $ python3 client.py
HTTP/1.1 200 OK
Content-Type: text/html

<ul><li><a href=http://127.0.0.1:8080/products/0>Fluent Python: Clear, Concise, and Effective Programming</a></li><li><a href=http://127.0.0.1:8080/products/1>Introducing Python: Modern Computing in Simple Packages</a></li></ul>

> $
```

## Homework

The TCP parser implementation can be found in `homework.py`.

For running the parser use `python3 homework.py`.

This is a parser that operates on a queue-based system. It systematically explores all pages and extracts URLs (href links) from each page, continuing this process recursively until no more sublinks are found (queue is empty). The client for this web scraper establishes a connection with the server using sockets and relies on TCP as its primary communication protocol.

When parsing simple pages, it saves their content as html files in the `./pages` directory.

For example, when parsing products listing page, it will save the content as `products.html` in the following format:

```html
<ul>
    <li><a href=http://127.0.0.1:8080/products/0>Fluent Python: Clear, Concise, and Effective Programming</a></li>
    <li><a href=http://127.0.0.1:8080/products/1>Introducing Python: Modern Computing in Simple Packages</a></li>
</ul>
```

For specific product, it will save the content in a file `products_x.html`, where `x = 0, 1, ...`. To exemplify, for `/products/0` path, the page content will be saved in `products_0.html` file, and so on.

From product pages, the product details are placed in a dictionary and accumulated throughout the all scrapping process in a list which is very simmilar to `data.json`. The json-ified result is stored in `data_homework.json` file.
