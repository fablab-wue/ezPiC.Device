"""
Web Plugin for Gateway-Pages
"""
from com.Globals import *

from web.MicroWebSrv.microWebSrv import MicroWebSrv

import com.Tool as Tool
import web.Web as Web

#######

@MicroWebSrv.route('/gateways')
def web_gateways(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'gateway.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    ret.sort(key=lambda x: x['NAME'].upper())

    vars = {}
    vars['menu'] = 'gateways'
    vars['gateway_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/gateways.html', vars=vars)

#######

@MicroWebSrv.route('/gateways/stage/')
def web_gateways_list(httpClient, httpResponse):
    """ TODO """

    err, ret = Web.command(httpResponse, 'gateway.stage.list')
    if err:
        Web.flash_error(httpResponse, err, ret)
        ret = []

    ret.sort(key=lambda x: x['PNAME'].upper())

    vars = {}
    vars['menu'] = 'gateways'
    vars['gateway_list'] = ret

    return httpResponse.WriteResponsePyHTMLFile('web/www/gateways_list.html', vars=vars)

#######

@MicroWebSrv.route('/gateways/add/<ezPID>/')
def web_gateway_add(httpClient, httpResponse, args):
    """ TODO """
    ezPID = args['ezPID']

    params = {'ezPID': ezPID}
    err, ret = Web.command(httpResponse, 'gateway.add', items=params)
    if err:
        Web.flash_error(httpResponse, err, ret, ezPID)
    else:
        Web.command(httpResponse, 'save')
        msg = 'Gateway "{}" added'.format(ezPID)
        httpResponse.FlashMessage(msg, 'info')
        return httpResponse.WriteResponseRedirect('/gateways/edit/'+str(ret))

    return httpResponse.WriteResponseRedirect('/gateways')

#######

@MicroWebSrv.route('/gateways/edit/<idx>/')
@MicroWebSrv.route('/gateways/edit/<idx>/', 'POST')
def web_gateway_edit(httpClient, httpResponse, args):
    """ TODO """
    idx = int(args['idx'])

    err, ret = Web.command(httpResponse, 'gateway.getparams', index=idx)
    if err:
        Web.flash_error(httpResponse, err, ret, idx)
        return httpResponse.WriteResponseRedirect('/gateways')

    params = {}
    params.update(ret)

    if httpClient.GetRequestMethod() == 'POST':
        formParams = httpClient.ReadRequestPostedFormData()        
        if formParams:
            formParams['ENABLE'] = 'ENABLE' in formParams   # checkbox -> bool
            params.update(formParams)
        err, ret = Web.command(httpResponse, 'gateway.setparams', index=idx, params=formParams)
        if not err:
            err, ret = Web.command(httpResponse, 'save')
        if err:
            Web.flash_error(httpResponse, err, ret, idx)
        else:
            httpResponse.FlashMessage('Settings saved', 'info')
    else: # GET
        pass

    vars = {}
    vars['menu'] = 'gateways'
    vars['index'] = idx
    vars.update(params)

    err, html = Web.command(httpResponse, 'gateway.gethtml', index=idx)

    return httpResponse.WriteResponsePyHTMLFile(html, vars=vars)

#######

@MicroWebSrv.route('/gateways/del/<idx>/')
def web_gateway_del(httpClient, httpResponse, args):
    """ TODO """
    idx = int(args['idx'])

    err, ret = Web.command(httpResponse, 'gateway.delete', index=idx)
    if err:
        Web.flash_error(httpResponse, err, ret, idx)
    else:
        err, ret = Web.command(httpResponse, 'save')
        msg = 'Gateway instance deleted'
        httpResponse.FlashMessage(msg, 'info')

    return httpResponse.WriteResponseRedirect('/gateways')

#######
