"""
MCP Server for Campus Faculty Connector
Designed to work with Google AI Studio via Render/Railway
"""

import os
import logging
from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize MCP server for Google AI Studio
mcp = FastMCP("Facultad-Agent-Connector")

# Read credentials securely from environment
CAMPUS_USER = os.getenv("CAMPUS_USER")
CAMPUS_PASS = os.getenv("CAMPUS_PASSWORD")
CAMPUS_URL = os.getenv("CAMPUS_URL", "https://campus.example.com")  # Configure your campus URL

# Session management for campus login
campus_session: Optional[requests.Session] = None


def init_campus_session() -> bool:
    """Initialize and authenticate session with campus"""
    global campus_session
    
    if not CAMPUS_USER or not CAMPUS_PASS:
        logger.error("Campus credentials not configured")
        return False
    
    try:
        campus_session = requests.Session()
        # TODO: Implement your specific campus login logic
        # Example: campus_session.post(f"{CAMPUS_URL}/login", data={...})
        logger.info("Campus session initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize campus session: {str(e)}")
        return False


@mcp.tool()
def get_enrolled_courses() -> str:
    """
    Access the faculty campus and return the list of active courses for the user.
    Returns a formatted string with enrolled courses.
    """
    if not CAMPUS_USER or not CAMPUS_PASS:
        logger.warning("Campus credentials not configured")
        return "Error: Campus credentials not configured in cloud environment. Please set CAMPUS_USER and CAMPUS_PASSWORD."
    
    try:
        # Initialize session if needed
        if campus_session is None:
            if not init_campus_session():
                return "Error: Could not authenticate with campus"
        
        # TODO: Replace with actual campus API/scraping logic
        # Example with requests:
        # response = campus_session.get(f"{CAMPUS_URL}/api/courses")
        # courses = response.json()
        
        # Simulated response for testing
        courses = [
            {"id": "1", "name": "Sociología", "status": "active"},
            {"id": "2", "name": "Trabajo Social", "status": "active"}
        ]
        
        # Format courses for AI agent
        courses_text = "Cursos inscritos:\n"
        for course in courses:
            courses_text += f"[{course['id']}] {course['name']} ({course['status']})\n"
        
        logger.info(f"Retrieved {len(courses)} courses for user {CAMPUS_USER}")
        return courses_text
        
    except Exception as e:
        logger.error(f"Error retrieving courses: {str(e)}")
        return f"Error retrieving courses: {str(e)}"


@mcp.tool()
def get_pending_assignments(course_id: str) -> str:
    """
    Get pending tasks and readings from campus for a specific course.
    
    Args:
        course_id: The course ID to retrieve assignments for
    
    Returns:
        Formatted string with pending assignments
    """
    if not course_id:
        return "Error: course_id parameter is required"
    
    try:
        if campus_session is None:
            if not init_campus_session():
                return "Error: Could not authenticate with campus"
        
        # TODO: Replace with actual campus API/scraping logic
        # Example: response = campus_session.get(f"{CAMPUS_URL}/api/courses/{course_id}/assignments")
        
        # Simulated response for testing
        assignments_map = {
            "1": [
                {"title": "Leer Unidad 2", "due_date": "2024-08-31", "type": "reading"},
                {"title": "Entregar TP de campo", "due_date": "2024-08-31", "type": "assignment"}
            ],
            "2": [
                {"title": "Participar en foro de debate", "due_date": "ongoing", "type": "forum"}
            ]
        }
        
        assignments = assignments_map.get(course_id, [])
        
        if not assignments:
            logger.warning(f"No assignments found for course {course_id}")
            return f"No pending assignments found for course ID {course_id}"
        
        # Format assignments for AI agent
        result = f"Tareas pendientes para curso {course_id}:\n"
        for assignment in assignments:
            result += f"- {assignment['title']} (Vence: {assignment['due_date']}) [{assignment['type']}]\n"
        
        logger.info(f"Retrieved {len(assignments)} assignments for course {course_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving assignments for course {course_id}: {str(e)}")
        return f"Error retrieving assignments: {str(e)}"


@mcp.tool()
def get_course_details(course_id: str) -> str:
    """
    Get detailed information about a specific course.
    
    Args:
        course_id: The course ID
    
    Returns:
        Formatted string with course details
    """
    if not course_id:
        return "Error: course_id parameter is required"
    
    try:
        # TODO: Implement actual course details retrieval
        details_map = {
            "1": {
                "name": "Sociología",
                "professor": "Dr. Juan Pérez",
                "description": "Estudio de estructuras y dinámicas sociales",
                "credits": 4,
                "schedule": "Lunes y Miércoles 10:00-12:00"
            },
            "2": {
                "name": "Trabajo Social",
                "professor": "Dra. María García",
                "description": "Intervención social y metodologías de TS",
                "credits": 5,
                "schedule": "Martes y Jueves 14:00-16:00"
            }
        }
        
        course = details_map.get(course_id)
        if not course:
            return f"No course found with ID {course_id}"
        
        result = f"Detalles del curso {course_id}:\n"
        result += f"Nombre: {course['name']}\n"
        result += f"Profesor: {course['professor']}\n"
        result += f"Descripción: {course['description']}\n"
        result += f"Créditos: {course['credits']}\n"
        result += f"Horario: {course['schedule']}\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving course details: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool()
def get_grades(course_id: Optional[str] = None) -> str:
    """
    Get grades for all courses or a specific course.
    
    Args:
        course_id: Optional specific course ID. If not provided, returns all grades.
    
    Returns:
        Formatted string with grades
    """
    try:
        # TODO: Implement actual grades retrieval
        grades_data = {
            "1": {"course": "Sociología", "grade": "8.5", "status": "passed"},
            "2": {"course": "Trabajo Social", "grade": "9.0", "status": "passed"}
        }
        
        if course_id:
            grade = grades_data.get(course_id)
            if not grade:
                return f"No grades found for course {course_id}"
            return f"Calificación en {grade['course']}: {grade['grade']}/10 - {grade['status']}"
        
        result = "Calificaciones actuales:\n"
        for cid, grade in grades_data.items():
            result += f"- {grade['course']}: {grade['grade']}/10\n"
        
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving grades: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool()
def health_check() -> str:
    """
    Check server health and campus connectivity.
    
    Returns:
        Status information
    """
    status = {
        "server": "online",
        "campus_configured": CAMPUS_USER is not None,
        "mcp_version": "1.0"
    }
    
    return f"Servidor MCP en línea. Estado: {status}"


if __name__ == "__main__":
    logger.info("Starting MCP Campus Connector Server")
    logger.info(f"Campus User: {CAMPUS_USER if CAMPUS_USER else 'Not configured'}")
    
    # Run the MCP server with SSE transport for Google AI Studio compatibility
    # The server will be accessible at http://localhost:5000
    # and the SSE endpoint will be at http://localhost:5000/sse
    mcp.run(transport="sse")
