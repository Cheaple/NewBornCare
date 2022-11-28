from sqlalchemy import and_

from app.extensions import db
from app.models import Tool


class ToolService():
    def get_tool_list(self):
        try:
            content_result = db.session.query(
                Tool.id,
                Tool.name,
            ).all()
            tool_list = [dict(zip(result.keys(), result))
                for result in content_result]
            return tool_list, "ok", True
        except Exception as e:
            print(e)
            return None, "error", False

    def add_tool(self, name):
        try:
            tool = Tool(name = name)
            db.session.add(tool)
            db.session.commit()
            return tool.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "tool already exists", False

    def update_tool(self, id, name = None):
        try:
            tool = Tool.query.get(id)
            if name:
                tool.name = name
            db.session.commit()
            return tool.id, "ok", True
        except Exception as e:
            print(e)
            return 0, "error", False
