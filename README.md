# Client–Server Computing

## 📌 Introduction
Client–Server computing is a distributed application model that separates roles into two entities:  
- **Client** → The requester of services (e.g., a chat application user).  
- **Server** → The provider of services (e.g., a central system that manages multiple clients).  

This model is the foundation of many systems such as chat applications, web browsers, and database servers.  

---

## 🖥️ How It Works
1. The **server** starts and listens for incoming client connections.  
2. A **client** connects to the server using its IP address and port number.  
3. Clients send messages → the server receives them → the server forwards them to other clients.  
4. The system allows multiple clients to communicate in real time.  

---

## ⚙️ Features
- Multi-client chat system using **TCP sockets**.  
- Username registration with duplicate checking.  
- Colored terminal output for better readability.  
- Graceful exit command (`tata`).  
- Handles unexpected disconnections.  

---