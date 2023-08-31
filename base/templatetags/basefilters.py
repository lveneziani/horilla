from django.template.defaultfilters import register
from django import template
from employee.models import Employee, EmployeeWorkInformation
from django.core.paginator import Page,Paginator



def paginator_qry(qryset,page_number):
    """
    This method is used to paginate queryset 
    """
    paginator = Paginator(qryset, 50) 
    qryset = paginator.get_page(page_number)
    return qryset


register = template.Library()
@register.filter(name='cancel_request')
def cancel_request(user,request):
    employee = user.employee_get
    employee_manages = employee.reporting_manager.all()
    return bool(
        request.employee_id == employee
        or user.has_perm('perms.base.cancel_worktyperequest')
        or user.has_perm('perms.base.cancel_shiftrequest')
        or employee_manages.exists()
    )

@register.filter(name='update_request')
def update_request(user,request):
    employee = user.employee_get
    return bool(
        not request.canceled
        and not request.approved
        and (
            employee == request.employee_id
            or user.has_perm('perms.base.change_worktyperequest')
            or user.has_perm('perms.base.change_shiftrequest')
        )
    )

@register.filter(name='is_reportingmanager')
def is_reportingmanager(user):
    """
    This method will return true if the user employee profile is reporting manager to any employee
    """
    employee = Employee.objects.filter(employee_user_id=user).first()
    return EmployeeWorkInformation.objects.filter(reporting_manager_id=employee).exists()



@register.filter(name='filtersubordinates')
def filtersubordinates(user):
    """
    This method returns true if the user employee has corresponding related reporting manager object in EmployeeWorkInformation model
    args:
        user    : request.user
    """
    employee =user.employee_get
    employee_manages = employee.reporting_manager.all()
    return employee_manages.exists()


@register.filter(name='clean_field')
def remove_id_suffix(value):
    if value.endswith("_id"):
        return value[:-3]
    
    return value.replace('_', ' ')
