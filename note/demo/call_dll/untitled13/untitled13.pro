#-------------------------------------------------
#
# Project created by QtCreator 2022-05-09T10:53:33
#
#-------------------------------------------------

QT       -= core gui

TARGET = untitled13
TEMPLATE = lib

DEFINES += UNTITLED13_LIBRARY

SOURCES += untitled13.cpp

HEADERS += untitled13.h

unix {
    target.path = /usr/lib
    INSTALLS += target
}
