# Azure Service Bus Publisher and Subscriber (Connection String Based)

This project demonstrates how to use Azure Service Bus to publish and subscribe to messages using a `connection string`.

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
    cd azure-service-bus-pub-sub/connection_string_based/
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

### Configuration
Create a `.env` file in the root of your project & insert your `connection string`, `topic name` & `subscription name`.

Here's an example:
```env
CONNECTION_STR_PUBLISH = 'your_publish_connection_string_name'
CONNECTION_STR_LISTEN = 'your_listen_connection_string_name'
TOPIC_NAME = 'your_topic_name'
SUBSCRIPTION_NAME = 'your_topic_subscription_name'
```


Before running the project, add the project directory to your `PYTHONPATH`:
```bash
export PYTHONPATH=$PYTHONPATH:/path/to/your/azure-service-bus-pub-sub
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
