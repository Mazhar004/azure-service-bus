# Azure Service Bus Publisher and Subscriber

This project demonstrates how to use Azure Service Bus to `publish` and `subscribe` to messages using `passwordless authentication`.


## Getting Started

### Prerequisites

- Python `3.8` or higher
- `pip` (Python package installer)
- An `Azure account` with an active subscription

### Installation

1. `Clone` the repository:

    ```bash
    git clone https://github.com/Mazhar004/azure_databus.git
    ```
2. `Navigate` to the project directory:

    ```bash
    cd azure_databus/password_less/
    ```

3. Create a `virtual` environment:
    ```bash
    python3 -m venv venv
    ```
4. Activate the `virtual` environment:
   - On `Unix` or `MacOS`:

        ```bash
        source venv/bin/activate
        ```
5. Upgrade `pip`:
    ```bash
    pip install --upgrade pip setuptools
    ```

6. `Install` the required packages:
    ```bash
    pip install -r requirements.txt
    ```
7. Install `Azure CLI`:

    For `Linux`:

    - Follow the guidline [Link](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

    For `macOS`:

    ```bash
    brew update && brew install azure-cli
    ```

8. Login to `Azure`:

    ```bash
    az login
    ```
### Configuration
Create a `.env` file in the root of your project & insert your `fully qualified namespace`, `topic name` & `subscription name`.

Here's an example:
```env
FULLY_QUALIFIED_NAMESPACE = 'yout_data_bus_name.servicebus.windows.net'
TOPIC_NAME = 'your_topic_name'
SUBSCRIPTION_NAME = 'your_topic_subscription_name'
```


Before running the project, add the project directory to your `PYTHONPATH`:
```bash
export PYTHONPATH=$PYTHONPATH:/path/to/your/azure_databus
```

### Usage
#### Publisher
To publish a message, run the following command:
```bash
python publisher.py --msg "Your message here"
```

#### Subscriber
To start the subscriber, run the following command:
```bash
python subscriber.py
```
