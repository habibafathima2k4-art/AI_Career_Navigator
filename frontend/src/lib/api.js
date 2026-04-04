const fallbackApiUrl = "http://localhost:8000/api";
const tokenStorageKey = "ai-career-navigator-token";
const userStorageKey = "ai-career-navigator-user";

export function getApiBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL || fallbackApiUrl;
}

export function getStoredToken() {
  return window.localStorage.getItem(tokenStorageKey);
}

export function getStoredUser() {
  const raw = window.localStorage.getItem(userStorageKey);
  return raw ? JSON.parse(raw) : null;
}

export function persistAuthSession(token, user) {
  window.localStorage.setItem(tokenStorageKey, token);
  window.localStorage.setItem(userStorageKey, JSON.stringify(user));
}

export function clearAuthSession() {
  window.localStorage.removeItem(tokenStorageKey);
  window.localStorage.removeItem(userStorageKey);
}

async function apiRequest(path, options = {}) {
  const token = getStoredToken();
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || `API request failed with ${response.status}`);
  }

  return response.json();
}

export function fetchSkills() {
  return apiRequest("/skills");
}

export function submitAssessment(payload) {
  return apiRequest("/assessments", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function fetchRecommendations(assessmentId) {
  return apiRequest(`/assessments/${assessmentId}/recommendations`);
}

export function fetchAssessments() {
  return apiRequest("/assessments");
}

export function fetchCareer(careerId) {
  return apiRequest(`/careers/${careerId}`);
}

export function fetchResources({ careerId, skillId, limit } = {}) {
  const params = new URLSearchParams();
  if (careerId) params.set("career_id", careerId);
  if (skillId) params.set("skill_id", skillId);
  if (limit) params.set("limit", limit);
  const suffix = params.toString() ? `?${params.toString()}` : "";
  return apiRequest(`/resources${suffix}`);
}

export function registerUser(payload) {
  return apiRequest("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function loginUser(payload) {
  return apiRequest("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function fetchCurrentUser() {
  return apiRequest("/auth/me");
}

export function fetchAdminSkills() {
  return apiRequest("/admin/skills");
}

export function createAdminSkill(payload) {
  return apiRequest("/admin/skills", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateAdminSkill(skillId, payload) {
  return apiRequest(`/admin/skills/${skillId}`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function deleteAdminSkill(skillId) {
  return apiRequest(`/admin/skills/${skillId}`, {
    method: "DELETE"
  });
}

export function fetchAdminCareers() {
  return apiRequest("/admin/careers");
}

export function createAdminCareer(payload) {
  return apiRequest("/admin/careers", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateAdminCareer(careerId, payload) {
  return apiRequest(`/admin/careers/${careerId}`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function deleteAdminCareer(careerId) {
  return apiRequest(`/admin/careers/${careerId}`, {
    method: "DELETE"
  });
}

export function fetchAdminResources() {
  return apiRequest("/admin/resources");
}

export function fetchAdminAnalytics() {
  return apiRequest("/admin/analytics");
}

export function createAdminResource(payload) {
  return apiRequest("/admin/resources", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export function updateAdminResource(resourceId, payload) {
  return apiRequest(`/admin/resources/${resourceId}`, {
    method: "PUT",
    body: JSON.stringify(payload)
  });
}

export function deleteAdminResource(resourceId) {
  return apiRequest(`/admin/resources/${resourceId}`, {
    method: "DELETE"
  });
}
