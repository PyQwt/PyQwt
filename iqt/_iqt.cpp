// _iqt.cpp -- marries PyQt with the Python command line interpreter.
//
// Copyright (C) 2003 Gerard Vermeulen
//
// This file is part of PyQwt.
//
// PyQwt is free software; you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the Free Software
// Foundation; either version 2 of the License, or (at your option) any later
// version.
//
// PyQwt is distributed in the hope that it will be useful, but WITHOUT ANY
// WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// PyQwt; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
// Suite 330, Boston, MA 02111-1307, USA.
//
// In addition, as a special exception, Gerard Vermeulen gives permission to
// link PyQwt with commercial, non-commercial or educational versions of Qt,
// PyQt and sip, and distribute PyQwt in this form, provided that equally
// powerful versions of Qt, PyQt and sip have been released under the terms
// of the GNU General Public License.
//
// If PyQwt is dynamically linked with commercial, non-commercial or
// educational versions of Qt, PyQt and sip, PyQwt becomes a free plug-in
// for a non-free program.


#include <Python.h>

#ifndef MS_WIN32
extern "C" void Py_GetArgcArgv(int *argc, char ***argv);
#else
#error "MicroSoft Windows is unsupported because it has no readline module"
#endif


#include <qapplication.h>
static QApplication *mine = 0;

static int iqt_event_handler(void)
{
    qApp->processEvents();
    return 0;
}

static PyObject *
iqt_enable_hook(PyObject *)
{
    if (!qApp) {
	int argc;
	char **argv;
	Py_GetArgcArgv(&argc, &argv);
	mine = new QApplication(argc, argv);
    }

    if (mine) {
	PyOS_InputHook = iqt_event_handler;
	Py_INCREF(Py_None);
	return Py_None;
    } else {
	PyErr_SetString(
	    PyExc_RuntimeError,
	    "refuses to hook event processing for a 'strange' QApplication.");
	return 0;
    }
}

static PyObject *
iqt_interacting(PyObject *)
{
    return Py_BuildValue("i", Py_InteractiveFlag ? 1 : 0); 
}

static PyObject *
iqt_disable_hook(PyObject *)
{
    PyOS_InputHook = 0;

    Py_INCREF(Py_None);
    return Py_None;
}

static struct PyMethodDef IQtPyModuleMethods[] = {
    {"disable_hook", (PyCFunction)iqt_disable_hook, METH_NOARGS, 0},
    {"enable_hook",  (PyCFunction)iqt_enable_hook,  METH_NOARGS, 0},
    {"interacting",  (PyCFunction)iqt_interacting,  METH_NOARGS, 0},
    {0, 0},
};

extern "C" DL_EXPORT(void)
init_iqt(void)
{
    Py_InitModule("_iqt", IQtPyModuleMethods);
}

// Local variables:
// mode: C++
// c-file-style: "stroustrup" 
// compile-command: "python setup.py build"
// End:
