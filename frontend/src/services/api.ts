export interface ResumeRewriteRequest {
  job_description: string;
  provider: string;
  model: string;
  resume_name: string;
  template_name: string;
  company_name?: string;
  location?: string;
  role?: string;
}

export interface ResumeRewriteResponse {
  resume_data: any;
  docx_path: string;
  pdf_path: string;
  pdf_url?: string;
}

export const rewriteResume = async (data: ResumeRewriteRequest): Promise<ResumeRewriteResponse> => {
  const payload = {
    job_description: data.job_description,
    provider: data.provider,
    model: data.model,
    resume_name: data.resume_name,
    template_name: data.template_name,
    ...(data.company_name && { company_name: data.company_name }),
    ...(data.location && { location: data.location }),
    ...(data.role && { role: data.role }),
  };

  const response = await fetch("http://localhost:8080/api/v1/resume/rewrite", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(err || "Failed to generate resume");
  }

  return await response.json();
};

export interface SaveApplicationRequest {
  job_description: string;
  provider: string;
  model: string;
  resume_name: string;
  template_name?: string;
  company_name?: string;
  location?: string;
  role?: string;
  pdf_path: string;
  docx_path: string;
}

export const saveApplication = async (data: SaveApplicationRequest) => {
  const response = await fetch("http://localhost:8080/api/v1/applications/save", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(err || "Failed to save application");
  }

  return await response.json();
};
