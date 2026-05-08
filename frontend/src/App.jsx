import { useState } from "react";
import axios from "axios";
import {
  Shield,
  Send,
  CheckCircle,
  Bot,
  User,
  AlertTriangle,
} from "lucide-react";
import "./App.css";

const API_URL =
  "https://cyberguard-ai-advisor-production.up.railway.app";

function RiskBadge({ risk }) {
  if (!risk) return null;

  const cls =
    risk === "High"
      ? "risk high"
      : risk === "Medium"
      ? "risk medium"
      : "risk low";

  return <span className={cls}>{risk} Risk</span>;
}

function formatAnswer(text) {
  if (!text) return null;

  return text.split("\n").map((line, index) => {
    const clean = line.trim();

    if (!clean) return <br key={index} />;

    const isSection =
      clean.endsWith(":") ||
      clean.toLowerCase().includes("explanation:") ||
      clean.toLowerCase().includes("key risks:") ||
      clean.toLowerCase().includes("recommended actions:") ||
      clean.toLowerCase().includes("final advice:");

    const isBullet = clean.startsWith("-");

    if (isSection) {
      return <h4 key={index}>{clean}</h4>;
    }

    if (isBullet) {
      return <li key={index}>{clean.replace("-", "").trim()}</li>;
    }

    return <p key={index}>{clean}</p>;
  });
}

function AssistantMessage({ result }) {
  const finalRisk = result?.final_decision?.final_risk;

  return (
    <div className="message assistant">
      <div className="avatar bot-avatar">
        <Bot size={18} />
      </div>

      <div className="bubble">
        <div className="bubble-header">
          <strong>CyberGuard</strong>
          <RiskBadge risk={finalRisk} />
        </div>

        {result?.priority === "incident_response" && (
          <div className="alert-box">
            <AlertTriangle size={18} />
            Immediate action required. Follow the steps carefully.
          </div>
        )}

        {result?.assistant_reply && (
          <p className="assistant-summary">
            {result.assistant_reply}
          </p>
        )}

        {result?.answer && (
          <div
            className="answer-content"
            lang={/[ء-ي]/.test(result.answer) ? "ar" : "en"}
          >
            {formatAnswer(result.answer)}
          </div>
        )}

        {result?.final_decision && (
          <div className="analysis-box">
            <h4>Final Decision</h4>

            <p>
              <strong>Risk:</strong>{" "}
              {result.final_decision.final_risk}
            </p>

            <p>
              <strong>Score:</strong>{" "}
              {result.final_decision.final_score}
            </p>

            <p>
              <strong>Recommendation:</strong>{" "}
              {result.final_decision.recommendation}
            </p>

            <h4>Reasons</h4>

            <ul>
              {result.final_decision.decision_reasons?.map(
                (reason, idx) => (
                  <li key={idx}>{reason}</li>
                )
              )}
            </ul>
          </div>
        )}

        {result?.ml_model_analysis && (
          <div className="mini-grid">
            <div className="mini-card">
              <span>ML Prediction</span>

              <strong>
                {result.ml_model_analysis.prediction ||
                  result.ml_model_analysis.label}
              </strong>
            </div>

            {"phishing_confidence" in result.ml_model_analysis && (
              <div className="mini-card">
                <span>Phishing Confidence</span>

                <strong>
                  {Math.round(
                    result.ml_model_analysis
                      .phishing_confidence * 100
                  )}
                  %
                </strong>
              </div>
            )}
          </div>
        )}

        {result?.rule_based_analysis && (
          <div className="analysis-box">
            <h4>Rule-based Signals</h4>

            <ul>
              {result.rule_based_analysis.reasons?.map(
                (reason, idx) => (
                  <li key={idx}>{reason}</li>
                )
              )}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

function UserMessage({ text }) {
  return (
    <div className="message user-message">
      <div className="bubble user-bubble">{text}</div>

      <div className="avatar user-avatar">
        <User size={18} />
      </div>
    </div>
  );
}

export default function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const examples = [
    "How can I protect myself from phishing?",
    "Can you check this link http://secure-login-bank.xyz ?",
    "Urgent! Your account has been suspended. Click now to verify your password.",
    "I clicked a suspicious link, what should I do now?",
    "How can I create a strong password?",
  ];

  async function sendMessage(text = message) {
    if (!text.trim()) return;

    const userText = text.trim();

    setChat((prev) => [
      ...prev,
      { role: "user", content: userText },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/chat/`,
        {
          message: userText,
        }
      );

      setChat((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.response,
        },
      ]);
    } catch (error) {
      console.error(error);

      setChat((prev) => [
        ...prev,
        {
          role: "assistant",
          content: {
            type: "error",
            answer:
              "Something went wrong. Make sure the backend server is running.",
          },
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="logo">
            <Shield size={28} />
          </div>

          <div>
            <h1>CyberGuard</h1>
            <p>AI Security Advisor</p>
          </div>
        </div>

        <div className="status">
          <CheckCircle size={18} />
          Backend Connected
        </div>

        <div className="tech-stack">
          ML + Rules + RAG + LLM
        </div>

        <div className="examples">
          <h3>Try examples</h3>

          {examples.map((ex, idx) => (
            <button
              key={idx}
              onClick={() => sendMessage(ex)}
            >
              {ex}
            </button>
          ))}
        </div>
      </aside>

      <main className="main">
        <section className="hero">
          <h1>CyberGuard AI Advisor</h1>

          <p>
            Chat with an AI-powered cybersecurity advisor
            that can analyze phishing emails, suspicious
            URLs, and answer defensive security questions.
          </p>
        </section>

        <section className="chat-window">
          {chat.length === 0 && (
            <div className="empty-state">
              <Shield size={50} />

              <h3>Start a security conversation</h3>

              <p>
                Ask a question, paste a suspicious email,
                or check a URL.
              </p>
            </div>
          )}

          {chat.map((item, idx) =>
            item.role === "user" ? (
              <UserMessage
                key={idx}
                text={item.content}
              />
            ) : (
              <AssistantMessage
                key={idx}
                result={item.content}
              />
            )
          )}

          {loading && (
            <div className="message assistant">
              <div className="avatar bot-avatar">
                <Bot size={18} />
              </div>

              <div className="bubble typing">
                CyberGuard is analyzing...
              </div>
            </div>
          )}
        </section>

        <section className="input-area">
          <textarea
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Ask CyberGuard anything about cybersecurity..."
          />

          <button
            onClick={() => sendMessage()}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Send"}

            <Send size={18} />
          </button>
        </section>
      </main>
    </div>
  );
}