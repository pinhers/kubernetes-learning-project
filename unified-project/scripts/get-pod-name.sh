#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: ./get-pod-name.sh [flask|nginx|file-server]"
    exit 1
fi

case $1 in
    "flask")
        kubectl get pods -l app=flask-backend -o jsonpath='{.items[0].metadata.name}'
        ;;
    "nginx") 
        kubectl get pods -l app=nginx-reverse-proxy -o jsonpath='{.items[0].metadata.name}'
        ;;
    "file-server")
        kubectl get pods -l app=file-server-persistent -o jsonpath='{.items[0].metadata.name}'
        ;;
    *)
        echo "Invalid service: $1"
        echo "Use: flask, nginx, or file-server"
        exit 1
        ;;
esac
