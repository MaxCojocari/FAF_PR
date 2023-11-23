# LAB8

In this laboratory exercise, I extended an existing CRUD service by adding two more instances, creating a distributed system with one Leader and two Followers. This setup is designed to demonstrate the implementation of the RAFT algorithm for Leader Election and to showcase different roles and capabilities of the Leader and Followers within the system.

## System Architecture

- **Leader Service**: Capable of handling both read (READ) and write (CREATE, UPDATE, DELETE) operations. It is responsible for forwarding write requests to the Followers;

- **Follower Services**: Limited to handling read requests. They only accept write requests forwarded by the Leader.

## Implementation of RAFT Algorithm

The RAFT algorithm is employed for determining the Leader among the services. The process is as follows:

1. **Initialization**: All services attempt to connect using UDP and bind to the connection;

2. **Leader Election**: Only one service succeeds in this step, becoming the Leader. The others automatically become Followers;

3. **Role Acknowledgment**: Followers send an 'Accept' message to the Leader, acknowledging its role;

4. **Exchange of Credentials**:

   - The Leader sends its HTTP credentials (IP, port, token for writes) to the Followers;

   - Followers, upon receiving this information, send back their HTTP credentials to the Leader;

5. **Credential Storage**: The Leader stores the Followers' credentials for future communication.

6. **HTTP Server Activation**: The HTTP server starts up, enabling communication between the Leader and Followers.

## Operational Dynamics

- **Followers**: Post-election, they handle only read requests from external sources;

- **Leader**: Manages all types of requests. For write operations, it forwards these requests to the Followers using the stored credentials.

## References

1. https://hackernoon.com/distributed-data-store-and-transaction-sagas

2. https://hackernoon.com/understanding-partitioned-services-in-distributed-systems

3. https://loud-orange-6fb.notion.site/Partition-Leader-Elections-and-re-elections-c0e9100c729b4fe4829c6025d4aae155?pvs=4
