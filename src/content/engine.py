class ContentManager:
    def __init__(self):
        self.projects = []

    def create_project(self, title: str, platform: str = "YouTube"):
        project = {
            "title": title,
            "platform": platform,
            "stage": "Scripting",
            "assets": []
        }
        self.projects.append(project)
        return {"status": "success", "project": project}

    def update_stage(self, title: str, new_stage: str):
        valid_stages = ["Scripting", "Editing", "Thumbnail", "Ready", "Published"]
        for p in self.projects:
            if p["title"].lower() == title.lower():
                if new_stage in valid_stages:
                    p["stage"] = new_stage
                    return {"status": "success", "updated_project": p}
                return {"status": "error", "message": f"Invalid stage. Choose from: {valid_stages}"}
        return {"status": "error", "message": "Project not found"}
