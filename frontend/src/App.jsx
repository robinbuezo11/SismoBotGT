import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import WelcomeScreen from './components/WelcomeScreen';

import { useChat } from './hooks/useChat';

export default function App() {
  const { messages, loading, sendMessage } = useChat();

  return (
    <div
      className="
        h-screen
        flex
        flex-col
        bg-gray-100
      "
    >
      <Header />

      <div className="flex-1 overflow-hidden flex flex-col">
        {
          messages.length === 0 ? (
            <WelcomeScreen onSelect={sendMessage} />
          ) : (
            <ChatWindow messages={messages} loading={loading} />
          )
        }
      </div>

      <ChatInput onSend={sendMessage} loading={loading} />
    </div>
  );
}