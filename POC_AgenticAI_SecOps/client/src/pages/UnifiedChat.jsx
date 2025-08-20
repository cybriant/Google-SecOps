import { useRef, useState, useEffect } from "react";
import { SendHorizonal, TrendingUp, LineChart, Vote, Newspaper, Copy } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import rehypeHighlight from 'rehype-highlight';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import { SERVER_URL } from '../providers/server';

const componentsMD = {
    h1: ({ node, ...props }) => (
        <h1 className="text-xl sm:text-2xl font-bold m-0 mb-2 sm:mb-3 mt-2 sm:mt-3" {...props} />
    ),
    h2: ({ node, ...props }) => (
        <h2 className="text-lg sm:text-xl font-semibold m-0 mb-1.5 sm:mb-2 mt-1.5 sm:mt-2" {...props} />
    ),
    h3: ({ node, ...props }) => (
        <h3 className="text-base sm:text-lg font-semibold m-0 mb-1.5 sm:mb-2 mt-1.5 sm:mt-2" {...props} />
    ),
    h4: ({ node, ...props }) => (
        <h4 className="text-sm sm:text-base font-medium m-0 mb-1 mt-1" {...props} />
    ),
    p: ({ node, ...props }) => (
        <p className="text-xs sm:text-sm leading-relaxed m-0 mb-1.5 sm:mb-2" {...props} />
    ),
    ul: ({ node, ...props }) => (
        <ul className="list-disc list-outside pl-3 sm:pl-4 text-xs sm:text-sm leading-relaxed m-0 my-1.5 sm:my-2 py-0" {...props} />
    ),
    ol: ({ node, ...props }) => (
        <ol className="list-decimal list-outside pl-3 sm:pl-4 text-xs sm:text-sm leading-relaxed m-0 my-1.5 sm:my-2 py-0" {...props} />
    ),
    li: ({ node, ...props }) => (
        <li className="leading-relaxed m-0 mb-0.5 sm:mb-1" {...props} />
    ),
    strong: ({ node, ...props }) => (
        <strong className="font-bold" {...props} />
    ),
    em: ({ node, ...props }) => (
        <em className="italic" {...props} />
    ),
    a: ({ node, ...props }) => (
        <a className="text-blue-400 hover:underline hover:text-blue-300" target="_blank" rel="noopener noreferrer" {...props} />
    ),
    blockquote: ({ node, ...props }) => (
        <blockquote className="border-l-4 border-gray-600 pl-2 sm:pl-3 py-0.5 sm:py-1 italic text-gray-300 leading-none m-0 my-1.5 sm:my-2" {...props} />
    ),
    code: ({ node, inline, ...props }) => {
        if (inline) {
            return (
                <code className="bg-gray-800 rounded px-1 sm:px-1.5 py-0.5 text-xs sm:text-sm font-mono text-green-400" {...props} />
            );
        }
        return (
            <pre className="bg-gray-800 rounded p-2 sm:p-3 text-xs sm:text-sm overflow-x-auto leading-none m-0 my-1.5 sm:my-2" {...props}>
                <code className="text-green-400">{props.children}</code>
            </pre>
        );
    },
    table: ({ node, ...props }) => (
        <div className="overflow-x-auto max-h-[60dvh] overflow-y-auto my-1.5 sm:my-2">
            <table className="w-full border-collapse border border-white/20 my-0 py-0" {...props} />
        </div>
    ),
    thead: ({ node, ...props }) => (
        <thead className="bg-[#1a1a1a]" {...props} />
    ),
    tbody: ({ node, ...props }) => (
        <tbody className="divide-y divide-white/10" {...props} />
    ),
    tr: ({ node, ...props }) => (
        <tr className="border-b border-white/5 hover:bg-white/5" {...props} />
    ),
    th: ({ node, ...props }) => (
        <th className="py-1.5 sm:py-2 px-2 sm:px-3 text-white/70 text-[10px] sm:text-xs font-medium text-left" {...props} />
    ),
    td: ({ node, ...props }) => (
        <td className="py-1.5 sm:py-2 px-2 sm:px-3 text-white text-[10px] sm:text-xs" {...props} />
    ),
};

function UnifiedChat() {
  const textareaRef = useRef(null);
  const bottomRef = useRef(null);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);
  
  // Generate unique user and session IDs
  const [userId] = useState(() => {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 8);
    return `u_${timestamp}_${random}`;
  });

  const [sessionId] = useState(() => {
    const timestamp = Date.now();
    const random = Math.random().toString(36).substring(2, 8);
    return `s_${timestamp}_${random}`;
  });

  useEffect(() => {
    const initializeSession = async () => {
      try {
        await fetch(`${SERVER_URL}/apps/secops_agent/users/${userId}/sessions/${sessionId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
      } catch (error) {
        console.error('Error initializing session:', error);
      }
    };

    initializeSession();
  }, [sessionId, userId]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    setIsLoading(true);
    setError(null);

    try {
      const newMessage = {
        user: input.trim(),
        response: "",
        time: new Date(),
        loading: true
      };
      
      setMessages(prev => [...prev, newMessage]);
      setInput("");

      // Initialize session
      try {
        const sessionResponse = await fetch(`${SERVER_URL}/apps/secops_agent/users/${userId}/sessions/${sessionId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            state: {}
          })
        });
        
        if (!sessionResponse.ok) {
          const errorData = await sessionResponse.json();
          if (!(sessionResponse.status === 400 && errorData.detail === `Session already exists: ${sessionId}`)) {
            throw new Error('Failed to initialize session');
          }
        }
      } catch (sessionError) {
        console.error('Session error:', sessionError);
      }

      // Use EventSource for SSE
      const response = await fetch(`${SERVER_URL}/run_sse`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          app_name: "secops_agent",
          user_id: userId,
          session_id: sessionId,
          new_message: {
            role: "user",
            parts: [{
              text: input.trim()
            }]
          },
          streaming: true
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response from server');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let accumulatedResponse = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const eventData = JSON.parse(line.slice(6));
              
              if (eventData.content?.parts) {
                const hasFunctionCall = eventData.content.parts.some(part => part.functionCall || part.functionResponse);
                if (!eventData.partial && !hasFunctionCall) {
                  continue;
                }

                const parts = eventData.content.parts.map(part => {
                  if (part.text) {
                    return part.text;
                  } else if (part.functionCall) {
                    return `<div class="bg-[#1a1a1a] border border-white/20 rounded-lg p-4 my-4 mx-0">
                      <div class="text-xs text-white/70 mb-1">Function Call</div>
                      <div class="text-sm text-white/90 font-semibold">${part.functionCall.name}</div>
                    </div>`;
                  } else if (part.functionResponse) {
                    return '';
                  }
                  return '';
                }).filter(Boolean).join('\n');

                if (parts) {
                  accumulatedResponse += parts;
                  setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMessage = { ...newMessages[newMessages.length - 1] };
                    lastMessage.response = accumulatedResponse;
                    newMessages[newMessages.length - 1] = lastMessage;
                    return newMessages;
                  });
                }
              }
            } catch (e) {
              console.error('Error parsing SSE data:', e);
            }
          }
        }
      }

      // Update final message state
      setMessages(prev => {
        const newMessages = [...prev];
        const lastMessage = { ...newMessages[newMessages.length - 1] };
        lastMessage.loading = false;
        newMessages[newMessages.length - 1] = lastMessage;
        return newMessages;
      });

    } catch (error) {
      console.error('Error in chat:', error);
      setError('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.focus();
        }
      }, 100);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="bg-[#000000] flex flex-col h-full">
      <div className="flex flex-col h-full w-full">
        <div className="w-[95%] sm:w-[85%] md:w-[75%] min-w-[280px] max-w-[800px] mx-auto pt-2 sm:pt-4 px-2 sm:px-3 flex-1 flex flex-col">
          <div className="text-3xl sm:text-4xl md:text-5xl font-extrabold mb-1 text-center">
            <span className="bg-gradient-to-r from-white via-gray-400 to-green-400 bg-clip-text text-transparent">
              Agentic AI SecOps POC
            </span>
          </div>
          
          {error && (
            <div className="text-red-500 mb-4 text-center">
              {error}
            </div>
          )}

          <div className="flex-1 flex flex-col min-h-0">
            <div className="flex-1 space-y-2 mb-4 overflow-y-auto">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={idx === messages.length - 1 ? "mb-4" : ""}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <h2 className="text-xl sm:text-2xl md:text-3xl font-bold text-white m-0">
                      {msg.user}
                    </h2>
                  </div>
                  <div className="text-lg text-white min-h-[24px]">
                    <ReactMarkdown
                      rehypePlugins={[rehypeHighlight, rehypeRaw]}
                      remarkPlugins={[remarkGfm]}
                      components={componentsMD}
                    >
                      {msg.response}
                    </ReactMarkdown>
                    {msg.loading && (
                      <div className="flex items-center py-1">
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-gray-400 border-t-blue-500" />
                        <span className="ml-2 text-xs text-white/50">Thinking…</span>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-2 mt-4 items-center">
                    <button className="p-0.5" title="Copy to clipboard" onClick={() => handleCopy(msg.response)}>
                      <Copy className="w-3 h-3 text-white/60" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
            <div ref={bottomRef} />
          </div>

          <div className="w-full mt-auto pt-4">
            <div className="min-h-[80px] max-h-[200px] w-full border border-white/30 rounded-lg shadow-lg p-2 sm:p-3 bg-[#1a1a1a] backdrop-blur-sm flex gap-2">
              <textarea
                ref={textareaRef}
                className={`flex-1 resize-none bg-transparent text-white outline-none text-base text-xs sm:text-base ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
                style={{
                  lineHeight: '1.5rem',
                  maxHeight: '150px',
                  overflow: 'auto'
                }}
                placeholder="Type your message to start a new chat..."
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                  }
                }}
                disabled={isLoading}
              />
              <button
                className={`px-2 sm:px-3 h-fit my-auto py-2 bg-[#2e3d5c] text-white rounded-lg transition-colors flex items-center justify-center ${
                  isLoading ? 'opacity-50 cursor-not-allowed' : ''
                }`}
                onClick={handleSend}
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
                ) : (
                  <SendHorizonal className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default UnifiedChat;
