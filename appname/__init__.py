'''
DamnCThatQT
Donia Tung (PM), Carol Pan, Taylor Wong, Queenie Xiang
SoftDev2 pd7
P02 - Fin
'''

#initializing...

    except KeyError:
        order = 'desc'
    if not (args['query'] or args['max_amt'] or len(cuisines) != 0):
        if args['location']:
            return redirect(url_for('rest_recc', location=args['location'])) # send location info
        else:
            return redirect(url_for('rest_recc'))
    rests = zomato.restaurant_search(args['query'],
            args['location'],
            args['radius'],
            args['max_amt'],
            cuisines,
            sort,
            order)
    return render_template("zomato_results.html",
            rests = rests['restaurants'],
            num = rests['results_shown'])

if __name__ == "__main__":
    #when we change to lamp stack, change debug to False
    app.debug = True
    app.run()
