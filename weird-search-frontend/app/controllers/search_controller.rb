class SearchController < ApplicationController
  def get
    @results = []
    params[:query].to_s.split(/\W+/) do |token|
      @results += Page.where("? = ANY(title_tokens)", token).or(Page.where("? = ANY(word_tokens)", token))
    end
  end
end
