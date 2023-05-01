# Unofficial BingChat API

This project provides an API for BingChat. The API allows users to access BingChat from Python.

![Chat Image](assets/chat.gif)

## Getting Started

### Prerequisites

-   Python 3
-   pip
-   BingChat whitelisted

### Installation

#### 1. From Source

1. Clone the repo

    ```sh
    git clone https://github.com/DarkMatter-999/BingChat-API.git
    ```

2. Install all the dependencies

    ```sh
    pip install -r requirements.txt
    ```

3. Add your BingChat Cookie to .env file

    ```env
    U_COOKIE = <YOUR-COOKIE>
    ```

    To get the cookie open your MS Egde browser and paste in the address bar, hit go and copy the cookie

    ```js
    javascript: prompt(
        "Cookie",
        `; ${document.cookie}`.split(`; _U=`).pop().split(";").shift()
    );
    ```

#### From Pip

1. To install this package simply run
    ```sh
    pip install bingchatapi
    ```

### Usage

Run this demo by running the main.py file

```sh
python main.py
```

### Contact

@ me on twitter at [@DarkMatter_999](https://twitter.com/darkmatter_999)
