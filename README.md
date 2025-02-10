# evhchatbot
Chatbot using gen ai 

Problem statement:
 1. We are going to build a chat bot. This chat bat would be similar to chatgpt.
 2. Backend would be built in fast api, frontend would be built in streamlit. 
 3. This chatbot should be able to have in memory conversations.
 4. This entire project should be easily transferable between different members. 

Next Steps: 
 1. Start Reasearch on the above.
 2. Prepare a Architecutre diagram for the above solution and present to mentor. Ensure each component in the diagram is justified. Consider future scalability.
 3. Ensure there are checks that confidential data is not submitted to the chat bot 



Step 1: Build the Image
   docker-compose build
Step 2: Start the Container
   docker-compose up -d
Step 3: Verify Running Containers
    docker ps
    
=>. Access the Services
    FastAPI Backend: http://localhost:8000/docs
    Streamlit Frontend: http://localhost:8501
=>. Stop and Remove the Container
    docker-compose down
