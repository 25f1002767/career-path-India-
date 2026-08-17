import React, { useState } from "react";
import { Key, X, Check, ExternalLink, ShieldCheck, Trash2, Info } from "lucide-react";

interface ApiKeyModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentApiKey: string;
  onSaveApiKey: (key: string) => void;
}

export const ApiKeyModal: React.FC<ApiKeyModalProps> = ({
  isOpen,
  onClose,
  currentApiKey,
  onSaveApiKey,
}) => {
  const [apiKeyInput, setApiKeyInput] = useState(currentApiKey);
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    onSaveApiKey(apiKeyInput.trim());
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 1200);
  };

  const handleClear = () => {
    setApiKeyInput("");
    onSaveApiKey("");
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 1000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white text-slate-900 rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative overflow-hidden">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-600 flex items-center justify-center shrink-0">
            <Key className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-900">Custom Gemini API Key</h2>
            <p className="text-xs text-slate-500">Bring Your Own Key (BYOK) — Free for Students</p>
          </div>
        </div>

        {/* Info Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4 mb-6 text-xs text-blue-900 space-y-2">
          <div className="flex items-center space-x-2 font-bold text-blue-950">
            <Info className="w-4 h-4 text-blue-600 shrink-0" />
            <span>Why connect your own key?</span>
          </div>
          <p className="leading-relaxed text-blue-800">
            Using your own free Gemini API key ensures your career recommendations are never slowed down or rate-limited by shared server traffic.
          </p>
        </div>

        {/* Instructions to get free key */}
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 mb-6 text-xs space-y-2.5">
          <div className="font-bold text-slate-900 flex items-center justify-between">
            <span>How to get a 100% Free Key (30 Seconds):</span>
            <a
              href="https://aistudio.google.com/app/apikey"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline flex items-center space-x-1 font-semibold"
            >
              <span>Google AI Studio</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
          <ol className="list-decimal list-inside space-y-1 text-slate-600 pl-1">
            <li>Open Google AI Studio and sign in with any Google account.</li>
            <li>Click <strong>"Create API Key"</strong> and copy your key.</li>
            <li>Paste it below and click <strong>"Save Key"</strong>.</li>
          </ol>
        </div>

        {/* Key Form */}
        <form onSubmit={handleSave} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">
              Paste Your Gemini API Key
            </label>
            <input
              type="password"
              placeholder="AIzaSy..."
              value={apiKeyInput}
              onChange={(e) => setApiKeyInput(e.target.value)}
              className="w-full px-4 py-3 rounded-xl border border-slate-300 font-mono text-sm focus:outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition bg-slate-50 focus:bg-white"
            />
          </div>

          {/* Privacy note */}
          <div className="flex items-center space-x-2 text-[11px] text-slate-500">
            <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Stored securely in your local browser only. Never shared publicly.</span>
          </div>

          {/* Actions */}
          <div className="pt-2 flex items-center justify-between gap-3">
            {currentApiKey && (
              <button
                type="button"
                onClick={handleClear}
                className="px-4 py-2.5 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 text-xs font-semibold transition flex items-center space-x-1.5"
              >
                <Trash2 className="w-3.5 h-3.5" />
                <span>Remove Key</span>
              </button>
            )}

            <div className="flex items-center space-x-2 ml-auto">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 text-xs font-semibold transition"
              >
                Cancel
              </button>

              <button
                type="submit"
                className="px-6 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-extrabold shadow-sm transition flex items-center space-x-1.5"
              >
                {savedSuccess ? (
                  <>
                    <Check className="w-4 h-4 text-slate-950" />
                    <span>Saved!</span>
                  </>
                ) : (
                  <>
                    <Key className="w-4 h-4 text-slate-950" />
                    <span>Save Key</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
