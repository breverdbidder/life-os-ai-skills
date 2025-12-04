#!/usr/bin/env python3
"""
Life OS AI Skills System - Supabase Client
ADHD-Optimized Productivity Intelligence

Uses existing Supabase tables with Life OS specific activity_type/insight_type values.

Storage Strategy:
- activities (activity_type='lifeos_skill_task') → task documentation
- insights (insight_type='lifeos_ai_skill') → skills
- insights (insight_type='lifeos_skill_pattern') → patterns
- activities (activity_type='lifeos_skill_usage') → usage tracking

Created by: Ariel Shapira, Solo Founder - Everest Capital USA
"""

import os
import json
import requests
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any

# Credentials embedded for autonomous operation
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://mocerqjnksmhcjzxrewo.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vY2VycWpua3NtaGNqenhyZXdvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDUzMjUyNiwiZXhwIjoyMDgwMTA4NTI2fQ.fL255mO0V8-rrU0Il3L41cIdQXUau-HRQXiamTqp9nE")


@dataclass
class LifeOSTaskDoc:
    """Task documentation for Life OS AI Skills learning"""
    task_id: str
    title: str
    description: str
    task_type: str  # routine|goal|habit|intervention|tracking|automation
    category: str   # productivity|health|swimming|family|business|personal
    domain: str     # ARIEL|MICHAEL|FAMILY|BUSINESS
    complexity_score: int  # 1-10
    adhd_relevance: int   # 1-10 (how relevant to ADHD management)
    files_affected: List[str]
    implementation: Dict[str, Any]
    challenges: List[Dict[str, Any]]
    outcome: Dict[str, Any]
    skill_potential: int  # 1-10
    analyzed: bool = False
    created_at: Optional[str] = None


@dataclass
class LifeOSSkill:
    """Generated AI skill for Life OS"""
    skill_id: str
    name: str
    category: str  # productivity|health|swimming|family|business|automation
    domain: str    # ARIEL|MICHAEL|FAMILY|BUSINESS
    version: str
    description: str
    content: str
    pattern_sources: List[str]
    total_uses: int = 0
    success_rate: float = 0.0
    avg_time_saved: float = 0.0
    adhd_effectiveness: float = 0.0  # How effective for ADHD management
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class LifeOSSupabaseClient:
    """Client for Life OS AI Skills System using existing Supabase tables"""
    
    def __init__(self):
        self.url = SUPABASE_URL
        self.headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None, params: dict = None) -> dict:
        """Make authenticated request to Supabase"""
        url = f"{self.url}/rest/v1/{endpoint}"
        r = requests.request(method, url, headers=self.headers, json=data, params=params, verify=False, timeout=30)
        if r.status_code >= 400:
            raise Exception(f"Supabase error {r.status_code}: {r.text}")
        return r.json() if r.text else {}
    
    # ========== TASK DOCUMENTATION ==========
    
    def save_task(self, task: LifeOSTaskDoc) -> dict:
        """Save task documentation to activities table"""
        record = {
            "activity_type": "lifeos_skill_task",
            "platform": "life_os_skills",
            "domain": task.domain,
            "notes": json.dumps({
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "task_type": task.task_type,
                "category": task.category,
                "complexity_score": task.complexity_score,
                "adhd_relevance": task.adhd_relevance,
                "files_affected": task.files_affected,
                "implementation": task.implementation,
                "challenges": task.challenges,
                "outcome": task.outcome,
                "skill_potential": task.skill_potential,
                "analyzed": task.analyzed
            }),
            "focus_quality": task.complexity_score,
            "energy_level": task.adhd_relevance
        }
        return self._request("POST", "activities", record)
    
    def get_unanalyzed_tasks(self, limit: int = 50) -> List[dict]:
        """Get tasks not yet analyzed for patterns"""
        params = {
            "activity_type": "eq.lifeos_skill_task",
            "order": "created_at.desc",
            "limit": limit
        }
        results = self._request("GET", "activities", params=params)
        tasks = []
        for r in results:
            try:
                data = json.loads(r.get("notes", "{}"))
                if not data.get("analyzed", False):
                    tasks.append(data)
            except:
                pass
        return tasks
    
    # ========== AI SKILLS ==========
    
    def save_skill(self, skill: LifeOSSkill) -> dict:
        """Save AI skill to insights table"""
        record = {
            "insight_type": "lifeos_ai_skill",
            "title": skill.name,
            "description": skill.description,
            "source": "life_os_skills",
            "priority": "High",
            "status": "Active",
            "confidence": skill.success_rate,
            "action_taken": json.dumps({
                "skill_id": skill.skill_id,
                "category": skill.category,
                "domain": skill.domain,
                "version": skill.version,
                "content": skill.content,
                "pattern_sources": skill.pattern_sources,
                "total_uses": skill.total_uses,
                "avg_time_saved": skill.avg_time_saved,
                "adhd_effectiveness": skill.adhd_effectiveness
            }),
            "recurrence_count": skill.total_uses
        }
        return self._request("POST", "insights", record)
    
    def get_all_skills(self) -> List[dict]:
        """Get all Life OS AI skills"""
        params = {
            "insight_type": "eq.lifeos_ai_skill",
            "status": "eq.Active",
            "order": "created_at.desc"
        }
        results = self._request("GET", "insights", params=params)
        skills = []
        for r in results:
            try:
                data = json.loads(r.get("action_taken", "{}"))
                data["name"] = r.get("title")
                data["description"] = r.get("description")
                data["success_rate"] = r.get("confidence", 0)
                data["total_uses"] = r.get("recurrence_count", 0)
                skills.append(data)
            except:
                pass
        return skills
    
    # ========== METRICS ==========
    
    def get_system_metrics(self) -> dict:
        """Get overall system metrics"""
        skills = self.get_all_skills()
        
        total_uses = sum(s.get("total_uses", 0) for s in skills)
        total_time_saved = sum(s.get("avg_time_saved", 0) * s.get("total_uses", 0) for s in skills)
        avg_success = sum(s.get("success_rate", 0) for s in skills) / len(skills) if skills else 0
        avg_adhd = sum(s.get("adhd_effectiveness", 0) for s in skills) / len(skills) if skills else 0
        
        # Count tasks
        task_count_params = {"activity_type": "eq.lifeos_skill_task", "select": "id"}
        tasks = self._request("GET", "activities", params=task_count_params)
        
        # Group by domain
        domain_count = {}
        for s in skills:
            domain = s.get("domain", "PERSONAL")
            domain_count[domain] = domain_count.get(domain, 0) + 1
        
        return {
            "total_skills": len(skills),
            "total_uses": total_uses,
            "total_time_saved_hours": total_time_saved / 60,
            "avg_success_rate": avg_success,
            "avg_adhd_effectiveness": avg_adhd,
            "tasks_documented": len(tasks),
            "skills_by_domain": domain_count
        }


def get_client() -> LifeOSSupabaseClient:
    return LifeOSSupabaseClient()


if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    client = get_client()
    metrics = client.get_system_metrics()
    print("✅ Life OS AI Skills System Connected!")
    print(f"   Skills: {metrics['total_skills']}")
    print(f"   Tasks: {metrics['tasks_documented']}")
    print(f"   Time Saved: {metrics['total_time_saved_hours']:.1f}h")
    print(f"   ADHD Effectiveness: {metrics['avg_adhd_effectiveness']*100:.0f}%")
