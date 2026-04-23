"use client";

import { useState, useEffect } from "react";
import { rewriteResume, ResumeRewriteResponse, saveApplication } from "@/services/api";

const PROVIDERS = {
  openai: ["gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano", "gpt-5.3", "gpt-5.3-mini"],
  claude: ["claude-sonnet-4-6", "claude-opus-4-6", "claude-haiku-4-5-20251001", "claude-opus-4-5-20251101", "claude-sonnet-4-5-20250929", "claude-opus-4-1-20250805", "claude-opus-4-20250514", "claude-sonnet-4-20250514"],
  gemini: ["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
};

const RESUMES = ["ai_resume.json", "software_resume.json"];
const TEMPLATES = ["resume.docx"];

export default function Home() {
  const [jobDescription, setJobDescription] = useState("");
  const [provider, setProvider] = useState<keyof typeof PROVIDERS>("openai");
  const [model, setModel] = useState(PROVIDERS["openai"][0]);
  const [resumeName, setResumeName] = useState(RESUMES[0]);
  const [templateName, setTemplateName] = useState(TEMPLATES[0]);

  const [companyName, setCompanyName] = useState("");
  const [location, setLocation] = useState("");
  const [role, setRole] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [docxPath, setDocxPath] = useState<string | null>(null);
  const [pdfPath, setPdfPath] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleProviderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedProvider = e.target.value as keyof typeof PROVIDERS;
    setProvider(selectedProvider);
    setModel(PROVIDERS[selectedProvider][0]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobDescription) {
      setError("Job description is required.");
      return;
    }

    setLoading(true);
    setError(null);
    setPdfUrl(null);

    try {
      const response = await rewriteResume({
        job_description: jobDescription,
        provider,
        model,
        resume_name: resumeName,
        template_name: templateName,
        company_name: companyName,
        location,
        role
      });

      if (response.pdf_url) {
        setPdfUrl(response.pdf_url);
        setDocxPath(response.docx_path);
        setPdfPath(response.pdf_path);
        setSaveSuccess(null); // Reset save state on new generation
      } else {
        setError("Resume generated successfully, but no PDF URL was returned.");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveApplication = async () => {
    if (!jobDescription || !pdfPath || !docxPath) {
      setError("Resume must be generated before saving application.");
      return;
    }

    setSaving(true);
    setError(null);
    setSaveSuccess(null);

    try {
      const response = await saveApplication({
        job_description: jobDescription,
        provider,
        model,
        resume_name: resumeName,
        template_name: templateName,
        company_name: companyName,
        location,
        role,
        pdf_path: pdfPath,
        docx_path: docxPath
      });
      setSaveSuccess(`Application saved successfully in folder: ${response.folder}`);
    } catch (err: any) {
      setError(err.message || "Failed to save application");
    } finally {
      setSaving(false);
    }
  };

  if (!mounted) return null;

  return (
    <div
      className="min-h-screen bg-gray-950 text-gray-100 flex flex-col md:flex-row font-sans selection:bg-indigo-500/30"

    >
      <div className="w-full md:w-1/2 p-8 overflow-y-auto border-r border-gray-800">
        <h1 className="text-4xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400 tracking-tight">
          AI Resume Builder
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Job Description *</label>
            <textarea
              className="w-full h-40 p-4 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all resize-none shadow-inner"
              placeholder="Paste the target job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">AI Provider</label>
              <select
                className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all text-gray-100"
                value={provider}
                onChange={handleProviderChange}
              >
                {Object.keys(PROVIDERS).map((p) => (
                  <option key={p} value={p}>{p.toUpperCase()}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Model</label>
              <select
                className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all text-gray-100"
                value={model}
                onChange={(e) => setModel(e.target.value)}
              >
                {PROVIDERS[provider].map((m) => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Base Resume</label>
              <select
                className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all text-gray-100"
                value={resumeName}
                onChange={(e) => setResumeName(e.target.value)}
              >
                {RESUMES.map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Template</label>
              <select
                className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all text-gray-100"
                value={templateName}
                onChange={(e) => setTemplateName(e.target.value)}
              >
                {TEMPLATES.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="border-t border-gray-800 pt-6 mt-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-200">Optional Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Company Name</label>
                <input
                  type="text"
                  className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all"
                  placeholder="e.g. Acme Corp"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Target Role</label>
                <input
                  type="text"
                  className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all"
                  placeholder="e.g. Engineer"
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-400">Location</label>
                <input
                  type="text"
                  className="w-full p-3 bg-gray-900 border border-gray-700/50 rounded-xl focus:ring-2 focus:ring-indigo-500 transition-all"
                  placeholder="e.g. Remote"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 mt-8 rounded-xl font-bold text-lg shadow-lg transition-all ${loading
              ? "bg-indigo-600/50 cursor-not-allowed text-indigo-200"
              : "bg-indigo-600 hover:bg-indigo-500 hover:shadow-indigo-500/25 active:scale-[0.98] text-white"
              }`}
          >
            {loading ? "Generating Resume..." : "Generate Awesome Resume"}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-900/50 border border-red-800 rounded-xl text-red-200">
              {error}
            </div>
          )}

          {pdfUrl && (
            <button
              type="button"
              onClick={handleSaveApplication}
              disabled={saving || !!saveSuccess}
              className={`w-full py-4 mt-4 rounded-xl font-bold text-lg shadow-lg transition-all flex items-center justify-center gap-2 ${
                saveSuccess
                  ? "bg-emerald-600 cursor-default text-white"
                  : saving
                  ? "bg-emerald-600/50 cursor-not-allowed text-emerald-200"
                  : "bg-emerald-600 hover:bg-emerald-500 hover:shadow-emerald-500/25 active:scale-[0.98] text-white"
              }`}
            >
              {saveSuccess ? (
                <>
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Application Saved!
                </>
              ) : saving ? (
                "Saving Application..."
              ) : (
                "Save Application"
              )}
            </button>
          )}

          {saveSuccess && (
            <div className="mt-4 p-4 bg-green-900/50 border border-green-800 rounded-xl text-green-200 break-words">
              {saveSuccess}
            </div>
          )}
        </form>
      </div>

      <div className="w-full md:w-1/2 p-8 flex flex-col justify-center items-center relative overflow-hidden hidden md:flex bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-gray-900 via-gray-950 to-black">
        {/* Background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-600/10 rounded-full blur-[100px] pointer-events-none"></div>

        {loading ? (
          <div className="flex flex-col items-center justify-center space-y-6 z-10 w-full h-full max-w-2xl bg-gray-900/40 backdrop-blur-md rounded-3xl border border-gray-800/50 shadow-2xl">
            <div className="w-16 h-16 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
            <p className="text-indigo-300 font-medium animate-pulse text-lg tracking-wide">Brewing your tailored resume...</p>
          </div>
        ) : pdfUrl ? (
          <div className="w-full h-full max-w-4xl bg-white rounded-2xl overflow-hidden shadow-2xl shadow-indigo-500/10 z-10 border border-gray-800">
            <iframe
              src={pdfUrl}
              className="w-full h-full"
              title="Generated Resume"
            />
          </div>
        ) : (
          <div className="text-center z-10 p-16 border border-gray-800/50 bg-gray-900/40 rounded-3xl backdrop-blur-md max-w-md w-full shadow-2xl">
            <svg className="w-24 h-24 mx-auto text-gray-700/80 mb-8 drop-shadow-lg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h2 className="text-3xl font-bold text-gray-300 mb-3 tracking-tight">Preview Area</h2>
            <p className="text-gray-500 text-lg leading-relaxed">Your expertly tailored resume will appear elegantly here once generated.</p>
          </div>
        )}
      </div>

      {/* Mobile Preview Area */}
      {pdfUrl && (
        <div className="w-full h-[600px] md:hidden bg-white mt-8 border-t border-gray-800 shadow-2xl">
          <iframe
            src={pdfUrl}
            className="w-full h-full"
            title="Generated Resume"
          />
        </div>
      )}
    </div>
  );
}
