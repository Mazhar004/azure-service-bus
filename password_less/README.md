# Azure Service Bus Publisher and Subscriber (Password Less)

This project demonstrates how to use Azure Service Bus to `publish` and `subscribe` to messages using `passwordless authentication`.


## Getting Started

### Prerequisites

- Python `3.8` or higher
- `pip` (Python package installer)
- An `Azure account` with an active subscription

### Installation

1. `Clone` the repository:

    ```bash
    git clone https://github.com/Mazhar004/azure-service-bus-pub-sub.git
    ```
2. `Navigate` to the project directory:

    ```bash
    cd azure-service-bus-pub-sub/password_less/
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
Create a `.env` file in the root of your project & insert your secrets.
- `azure-service-bus-pub-sub/password_less/.env`

Here's an example:
```env
FULLY_QUALIFIED_NAMESPACE = 'yout_data_bus_name.servicebus.windows.net'
TOPIC_NAME = 'your_topic_name'
SUBSCRIPTION_NAME = 'your_topic_subscription_name'
```


Before running the project, make sure you are in sub-project directory:
```bash
azure-service-bus-pub-sub/password_less/
```

### Usage
#### Publisher
To publish a message, run the following command:
```bash
python publisher.py --msg "Your message here" --pubsub
```

#### Subscriber
To start the subscriber, run the following command:
```bash
python subscriber.py
```

### To RUN in Docker
### Configuration
Create a `.env` file in the root of your project & insert your secrets.
- `azure-service-bus-pub-sub/password_less/.env`

Here's an example:
```env
FULLY_QUALIFIED_NAMESPACE = 'yout_data_bus_name.servicebus.windows.net'
TOPIC_NAME = 'your_topic_name'
SUBSCRIPTION_NAME = 'your_topic_subscription_name'

# APP registration for Docker RUN
# Set environment variables for Azure Service Bus credentials
AZURE_CLIENT_ID= 'your_app_id'
AZURE_CLIENT_SECRET= 'your_client_secret'
AZURE_TENANT_ID= 'your_tenant_id'
```

### Build Image
- Subcriber
    ```bash
    docker build -t subscriber_tag_name .
    ```
- Publisher
    ```bash
    docker build -t publisher_tag_name . -f Dockerfile_Publisher
    ```  
### Run Image
- Subcriber
    ```bash
    docker run subscriber_tag_name python subscriber.py
    ```
- Publisher
    ```bash
    docker run publisher_tag_name python publisher.py --msg "your msg" --pubsub
    ```  