#!/usr/bin/python
import webapp
import urllib
import string

class proxy(webapp.webApp):
    cache = {}
    cache_entrada = {}
    cache_salida = {}
    serv_entrada = {}
    serv_salida = {}

    def parse(self, request):
        if not request:
            return '',''
        try:
            parametro = request.split(" ",2)[1][1:]
            cabecera = request.split("HTTP/1.1")[1][1:]
        except IndexError:
            parametro = None
        return parametro, cabecera
    def process(self, parsedArgument):
        [parsedRequest,cabecera] = parsedArgument
        if(parsedRequest in self.cache):
            httpCode = "200 OK"
            httpBody = "<html><head></head>"
            httpBody += "<body>" + self.cache[parsedRequest] +"</body></html>\r\n"
            print "cache"
        elif parsedRequest == None:
            httpCode = "404 Not Found"
            httpBody = "<html><head></head>"
            httpBody += "<body>Error de peticion</body></html>\r\n"
        elif len(parsedRequest.split('/')) == 1:
            try:
                httpCode = "200 OK"
                url_original = "http://" + parsedRequest
                f = urllib.urlopen (url_original)
                contenido = f.read()
                posicion1 = string.find(contenido,"<body ")
                posicion2 = string.find(contenido, ">", posicion1)

                original = "\n<a style= 'font-size: 20px;' href='" + url_original
                original += "'>Original</a>\n"

                url_reload = "http://localhost:1234/" + parsedRequest
                recarga = "<a style= 'font-size: 20px;' href='" + url_reload
                recarga += "'>Reload</a>\n"

                url_serv = "http://localhost:1234/serv/" + parsedRequest
                serv = "<a style= 'font-size: 20px;' href='" + url_serv
                serv += "'>Http servidor</a>\n"

                url_prox = "http://localhost:1234/prox/" + parsedRequest
                prox = "<a style= 'font-size: 20px;' href='" + url_prox
                prox +=  "'>HTTP proxy</a>\n"

                httpBody = contenido[:posicion1] + "<p>" + original + recarga
                httpBody += serv + prox + contenido[posicion2+1:] + "</p>"
                self.cache[parsedRequest]= httpBody
                self.cache_entrada[parsedRequest] = cabecera
                self.serv_entrada[parsedRequest] = str(f.info().headers)
                print "salimos"
            except IOError:
                httpBody = "Error: could not connect"
                httpCode = "404 Resource Not Available"
        else:
            if(parsedRequest.split("/")[0]=="prox"):
                httpCode = "200 OK"
                entrada = self.cache_entrada[parsedRequest.split("/")[1]]
                httpBody = "<html><head></head>"
                httpBody += "<body>" + entrada + "</body></html>\r\n"
            elif(parsedRequest.split("/")[0]=="serv"):
                httpCode = "200 OK"
                entrada = self.serv_entrada[parsedRequest.split("/")[1]]
                httpBody = "<html><head></head>"
                httpBody += "<body>" + entrada +"</body></html>\r\n"
            else:
                httpCode = ""
                httpBody = ""

        return (httpCode,httpBody)
if __name__ == "__main__":
    testcacheApp = proxy("localhost", 1234)
