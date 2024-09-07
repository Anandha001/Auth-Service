from models.enums import Role


ROLE_DESCRIPTION = {
    Role.OWNER: "The owner has full control over the organization, including managing roles, members, and settings.",
    Role.ADMIN: "The admin can manage users and settings, but might have limited access to organization-wide changes.",
    Role.MANAGER: "The manager can oversee team operations, manage resources, and handle day-to-day operations.",
    Role.MEMBER: "The member has standard access to resources and can participate in organizational activities.",
    Role.GUEST: "The guest has restricted access to resources, typically for temporary or external collaborators.",
}
