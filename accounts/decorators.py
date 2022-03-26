
from django.shortcuts import redirect, HttpResponse
from django.core.exceptions import PermissionDenied


def login_excluded(redirect_to):
    """ This decorator kicks authenticated users out of a view """ 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to) 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper



def doctor_patient_not_allowed_on_forensic(redirect_to):
    """ doctor_patient_not_allowed_on_forensic""" 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_doctor or request.user.is_patient:
                raise PermissionDenied 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def doctor_forensic_not_allowed_on_patient(redirect_to):
    """ doctor_forensic_not_allowed_on_patient""" 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_doctor or request.user.is_forensic:
                raise PermissionDenied 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

def patient_forensic_not_allowed_on_doctor(redirect_to):
    """ patient_forensic_not_allowed_on_doctor""" 
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_patient or request.user.is_forensic:
                raise PermissionDenied 
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper