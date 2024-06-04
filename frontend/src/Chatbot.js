import React, { useState } from 'react';
import './index.css';
import SendIcon from '@material-ui/icons/Send';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [showPlaceholder, setShowPlaceholder] = useState(true);

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { text: input, user: true };
      setMessages([...messages, userMessage]);
      setInput('');
      setShowPlaceholder(false);

      try {
        const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ sender: 'user', message: input }),
        });

        const data = await response.json();
        const botMessages = data.map((msg) => ({ text: msg.text, user: false }));
        setMessages((prevMessages) => [...prevMessages, ...botMessages]);
      } catch (error) {
        console.error('Error communicating with RASA:', error);
        setMessages((prevMessages) => [...prevMessages, { text: "Error communicating with bot", user: false }]);
      }
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    if (e.target.value.trim() === '') {
      setShowPlaceholder(true); // Show the placeholder when input is empty
    } else {
      setShowPlaceholder(false); // Hide the placeholder when input is not empty
    }
  };

  return (
    <div className={`chat-container ${'bg-white text-black'}`}>
      <div className="chat-header flex items-center"> {/* Add flex container */}
        <h1 style={{ marginRight: '30px' }}>FreshiesBot</h1>
      </div>
      <div className={`chat-history ${'bg-gray-100'}`}>
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.user ? 'user-message' : 'bot-message'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className={`chat-input-container ${'bg-gray-100'}`}>
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          className={`chat-input ${'bg-white text-black border-gray-300'}`}
          placeholder="Enter your message"
        />
        <button onClick={handleSend} className={`chat-button ${'bg-blue-500 text-white'}`} style={{ borderRadius: '15%', padding: '10px', marginLeft: '10px' }}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chatbot;

// import './Chatbot.css';
// import react, { useEffect, useState } from 'react';
// import {IoMdSend}  from 'react-icons/io';
// import {BiBot,BiUser} from 'react-icons/bi';

// function Chatbot(){
//     const [chat,setChat] = useState([]);
//     const [inputMessage,setInputMessage] = useState('');
//     const [botTyping,setbotTyping] = useState(false);

    
//    useEffect(()=>{
   
//         console.log("called");
//         const objDiv = document.getElementById('messageArea');
//         objDiv.scrollTop = objDiv.scrollHeight;
        
    
//     },[chat])

    


//     const handleSubmit=(evt)=>{
//         evt.preventDefault();
//         const name = "shreyas";
//         const request_temp = {sender : "user", sender_id : name , msg : inputMessage};
        
//         if(inputMessage !== ""){
            
//             setChat(chat => [...chat, request_temp]);
//             setbotTyping(true);
//             setInputMessage('');
//             rasaAPI(name,inputMessage);
//         }
//         else{
//             window.alert("Please enter valid message");
//         }
        
//     }


//     const rasaAPI = async function handleClick(name,msg) {
    
//         //chatData.push({sender : "user", sender_id : name, msg : msg});
        

//           await fetch('http://localhost:5005/webhooks/rest/webhook', {
//             method: 'POST',
//             headers: {
//               'Accept': 'application/json',
//               'Content-Type': 'application/json',
//               'charset':'UTF-8',
//             },
//             credentials: "same-origin",
//             body: JSON.stringify({ "sender": name, "message": msg }),
//         })
//         .then(response => response.json())
//         .then((response) => {
//             if(response){
//                 const temp = response[0];
//                 const recipient_id = temp["recipient_id"];
//                 const recipient_msg = temp["text"];        


//                 const response_temp = {sender: "bot",recipient_id : recipient_id,msg: recipient_msg};
//                 setbotTyping(false);
                
//                 setChat(chat => [...chat, response_temp]);
//                // scrollBottom();

//             }
//         }) 
//     }

//     console.log(chat);

//     const stylecard = {
//         maxWidth : '50rem',
//         border: '1px solid black',
//         paddingLeft: '0px',
//         paddingRight: '0px',
//         borderRadius: '30px',
//         boxShadow: '0 16px 20px 0 rgba(0,0,0,0.4)'

//     }
//     const styleHeader = {
//         height: '4.5rem',
//         borderBottom : '1px solid black',
//         borderRadius: '30px 30px 0px 0px',
//         backgroundColor: '#8012c4',

//     }
//     const styleFooter = {
//         //maxWidth : '32rem',
//         borderTop : '1px solid black',
//         borderRadius: '0px 0px 30px 30px',
//         backgroundColor: '#8012c4',
        
        
//     }
//     const styleBody = {
//         paddingTop : '10px',
//         height: '28rem',
//         overflowY: 'a',
//         overflowX: 'hidden',
        
//     }

//     return (
//       <div>
//         {/* <button onClick={()=>rasaAPI("shreyas","hi")}>Try this</button> */}
        

//         <div className="container">
//         <div className="row justify-content-center">
            
//                 <div className="card" style={stylecard}>
//                     <div className="cardHeader text-white" style={styleHeader}>
//                         <h1 style={{marginBottom:'0px'}}>AI Assistant</h1>
//                         {botTyping ? <h6>Bot Typing....</h6> : null}
                        
                        
                        
//                     </div>
//                     <div className="cardBody" id="messageArea" style={styleBody}>
                        
//                         <div className="row msgarea">
//                             {chat.map((user,key) => (
//                                 <div key={key}>
//                                     {user.sender==='bot' ?
//                                         (
                                            
//                                             <div className= 'msgalignstart'>
//                                                 <BiBot className="botIcon"  /><h5 className="botmsg">{user.msg}</h5>
//                                             </div>
                                        
//                                         )

//                                         :(
//                                             <div className= 'msgalignend'>
//                                                 <h5 className="usermsg">{user.msg}</h5><BiUser className="userIcon" />
//                                             </div>
//                                         )
//                                     }
//                                 </div>
//                             ))}
                            
//                         </div>
                
//                     </div>
//                     <div className="cardFooter text-white" style={styleFooter}>
//                         <div className="row">
//                             <form style={{display: 'flex'}} onSubmit={handleSubmit}>
//                                 <div className="col-10" style={{paddingRight:'0px'}}>
//                                     <input onChange={e => setInputMessage(e.target.value)} value={inputMessage} type="text" className="msginp"></input>
//                                 </div>
//                                 <div className="col-2 cola">
//                                     <button type="submit" className="circleBtn" ><IoMdSend className="sendBtn" /></button>
//                                 </div>
//                             </form>
//                         </div>
//                     </div>
//                 </div>
            
//         </div>
//         </div>

//       </div>
//     );
// }
  
// export default Chatbot;